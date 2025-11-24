from collections import defaultdict
from datetime import datetime, date
from typing import Optional, List
from calendar import monthrange

from app.repositories.reporte_repo import ReporteRepository
from app.schemas.reserva_schema import reservas_schema


class ReporteService:
    """
    Servicio para generar reportes de reservas y canchas.
    Contiene la lógica de negocio para procesar y formatear datos de reportes.
    """
    
    def __init__(self):
        self.reporte_repo = ReporteRepository()
    
    def _parse_date(self, s: Optional[str]) -> Optional[datetime]:
        """
        Convierte un string de fecha en formato YYYY-MM-DD a datetime.
        
        Args:
            s: String con formato YYYY-MM-DD
            
        Returns:
            datetime o None si el string es inválido o vacío
        """
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None
    
    def _parse_date_as_date(self, s: Optional[str]) -> Optional[date]:
        """
        Convierte un string de fecha en formato YYYY-MM-DD a date.
        
        Args:
            s: String con formato YYYY-MM-DD
            
        Returns:
            date o None si el string es inválido o vacío
        """
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return None
    
    def _month_iter(self, start: date, end: date) -> List[str]:
        """
        Genera una lista de meses en formato 'YYYY-MM' entre dos fechas.
        
        Args:
            start: Fecha de inicio
            end: Fecha de fin
            
        Returns:
            Lista de strings con formato 'YYYY-MM'
        """
        months = []
        y = start.year
        m = start.month
        while (y, m) <= (end.year, end.month):
            months.append(f"{y:04d}-{m:02d}")
            if m == 12:
                y += 1
                m = 1
            else:
                m += 1
        return months
    
    def get_reservas_por_cliente(
        self,
        q: Optional[str] = None,
        cliente_email: Optional[str] = None
    ) -> List[dict]:
        """
        Construye un listado de reservas agrupadas por cliente.
        
        Args:
            q: Búsqueda libre que compara con nombre o email del cliente (opcional)
            cliente_email: Búsqueda exacta por email del cliente (opcional)
        
        Returns:
            Lista de objetos con la forma:
            [
              {
                "cliente_email": "...",
                "cliente_nombre": "...",
                "cliente_telefono": "...",
                "reservas": [ ...reservas serializadas... ]
              },
              ...
            ]
        """
        reservas = self.reporte_repo.get_reservas_filtradas(
            cliente_email=cliente_email,
            q=q
        )
        
        grupos = defaultdict(list)
        info_cliente = {}
        
        for r in reservas:
            key = (r.cliente_email or "", r.cliente_nombre or "")
            grupos[key].append(r)
            # Guardar telefono (último valor disponible)
            info_cliente[key] = r.cliente_telefono
        
        resultado = []
        for (email, nombre), lista in grupos.items():
            resultado.append({
                "cliente_email": email,
                "cliente_nombre": nombre,
                "cliente_telefono": info_cliente.get((email, nombre)),
                "reservas": reservas_schema.dump(lista)
            })
        
        return resultado
    
    def get_reservas_por_cancha(
        self,
        cancha_id: Optional[int] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> List[dict]:
        """
        Construye un listado de reservas agrupadas por cancha dentro de un período.
        
        Args:
            cancha_id: Filtrar por una cancha específica (opcional)
            fecha_inicio: String en formato 'YYYY-MM-DD' (opcional)
            fecha_fin: String en formato 'YYYY-MM-DD' (opcional)
        
        Returns:
            Lista de objetos:
            [ {
                "cancha": { ... },
                "total_reservas": 3,
                "total_ingresos": "300.00",
                "reservas": [ ...reservas serializadas... ]
            }, ... ]
        """
        start_dt = self._parse_date(fecha_inicio)
        end_dt = self._parse_date(fecha_fin)
        if end_dt:
            # Incluir todo el día final
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
        
        reservas = self.reporte_repo.get_reservas_por_cancha(
            cancha_id=cancha_id,
            start_dt=start_dt,
            end_dt=end_dt
        )
        
        grupos = defaultdict(list)
        cancha_info = {}
        
        for r in reservas:
            key = r.cancha_id
            grupos[key].append(r)
            cancha_info[key] = r.cancha
        
        resultado = []
        for cancha_id_key, lista in grupos.items():
            total = sum([
                float(r.precio_total) if r.precio_total is not None else 0 
                for r in lista
            ])
            resultado.append({
                "cancha": {
                    "id": cancha_info[cancha_id_key].id,
                    "nombre": cancha_info[cancha_id_key].nombre,
                    "deporte": cancha_info[cancha_id_key].deporte,
                    "precio_hora": cancha_info[cancha_id_key].precio_hora,
                },
                "total_reservas": len(lista),
                "total_ingresos": f"{total:.2f}",
                "reservas": reservas_schema.dump(lista)
            })
        
        return resultado
    
    def get_canchas_mas_utilizadas(
        self,
        limit: int = 10,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> List[dict]:
        """
        Devuelve un ranking de canchas más utilizadas (por cantidad de reservas) 
        dentro de un periodo.
        
        Args:
            limit: Cantidad máxima de canchas a devolver
            fecha_inicio: String 'YYYY-MM-DD' para filtrar por inicio de timeslot
            fecha_fin: String 'YYYY-MM-DD' para filtrar por fin de timeslot
        
        Returns:
            Lista de objetos:
            [ { 
                "cancha": {id,nombre,deporte,precio_hora}, 
                "reservas_count": N, 
                "total_ingresos": "123.45",
                "porcentaje_utilizacion": "15.50%"
            }, ... ]
        """
        start_dt = self._parse_date(fecha_inicio)
        end_dt = self._parse_date(fecha_fin)
        if end_dt:
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
        
        # Obtener datos agregados
        rows = self.reporte_repo.get_canchas_mas_utilizadas_query(
            start_dt=start_dt,
            end_dt=end_dt,
            limit=limit
        )
        
        # Calcular total de reservas en el periodo (para porcentaje)
        total_reservas_period = self.reporte_repo.get_total_reservas_periodo(
            start_dt=start_dt,
            end_dt=end_dt
        )
        
        resultado = []
        for row in rows:
            cancha = self.reporte_repo.get_cancha_by_id(row.cancha_id)
            if not cancha:
                continue
            
            reservas_count = int(row.reservas_count)
            total_ingresos = float(row.total_ingresos or 0)
            porcentaje = 0.0
            if total_reservas_period > 0:
                porcentaje = (reservas_count / total_reservas_period) * 100.0
            
            resultado.append({
                "cancha": {
                    "id": cancha.id,
                    "nombre": cancha.nombre,
                    "deporte": cancha.deporte,
                    "precio_hora": cancha.precio_hora
                },
                "reservas_count": reservas_count,
                "total_ingresos": f"{total_ingresos:.2f}",
                "porcentaje_utilizacion": f"{porcentaje:.2f}%"
            })
        
        return resultado
    
    def get_utilizacion_mensual(
        self,
        cancha_id: Optional[int] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> dict:
        """
        Construye datos para un gráfico de utilización mensual de canchas.
        
        Args:
            cancha_id: Opcional para filtrar una sola cancha
            fecha_inicio: Rango en formato YYYY-MM-DD (opcional)
            fecha_fin: Rango en formato YYYY-MM-DD (opcional)
        
        Returns:
            JSON: {
              "months": ["2025-10","2025-11",...],
              "series": [
                 {"cancha": {id,nombre,deporte}, "data": [count_for_month,...] },
                 ...
              ]
            }
        """
        start_date = self._parse_date_as_date(fecha_inicio)
        end_date = self._parse_date_as_date(fecha_fin)
        
        # Obtener datos agregados
        rows = self.reporte_repo.get_utilizacion_mensual_query(
            cancha_id=cancha_id,
            start_date=start_date,
            end_date=end_date
        )
        
        if not rows:
            # Si no hay rows y no hay rango explícito, retornar estructura vacía
            if not (start_date and end_date):
                return {"months": [], "series": []}
        
        # Determinar rango de meses
        if start_date and end_date:
            months = self._month_iter(start_date, end_date)
        else:
            # Inferir desde los rows
            months_set = set(r.month for r in rows)
            if not months_set:
                return {"months": [], "series": []}
            min_month = min(months_set)
            max_month = max(months_set)
            start_date = datetime.strptime(min_month + "-01", "%Y-%m-%d").date()
            y, m = map(int, max_month.split('-'))
            last_day = monthrange(y, m)[1]
            end_date = date(y, m, last_day)
            months = self._month_iter(start_date, end_date)
        
        # Construir mapping cancha_id -> {month: count}
        data_map = {}
        cancha_ids = set()
        for r in rows:
            cid = int(r.cancha_id)
            cancha_ids.add(cid)
            data_map.setdefault(cid, {})[r.month] = int(r.count)
        
        # Si se filtró por cancha_id pero no hay rows, retornar serie vacía
        series = []
        if cancha_id and cancha_id not in cancha_ids:
            cancha = self.reporte_repo.get_cancha_by_id(cancha_id)
            if cancha:
                series.append({
                    "cancha": {
                        "id": cancha.id, 
                        "nombre": cancha.nombre, 
                        "deporte": cancha.deporte
                    },
                    "data": [0 for _ in months]
                })
            return {"months": months, "series": series}
        
        # Para cada cancha encontrada, construir serie alineada a months
        for cid in sorted(cancha_ids):
            cancha = self.reporte_repo.get_cancha_by_id(cid)
            if not cancha:
                continue
            counts = [data_map.get(cid, {}).get(month, 0) for month in months]
            series.append({
                "cancha": {
                    "id": cancha.id, 
                    "nombre": cancha.nombre, 
                    "deporte": cancha.deporte
                },
                "data": counts
            })
        
        return {"months": months, "series": series}
