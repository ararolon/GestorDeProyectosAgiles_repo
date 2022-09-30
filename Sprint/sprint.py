from Proyectos.models import Proyecto
from Sprint.models import Sprint, estadoSprint
from UserStories.models import UserStories

class sprintProyecto:
    
    def sprint_activo(id_proyecto):
        """
        Método para verificar si existe un sprint activo (En curso)
        """
        # return Sprint.objects.filter(id_proyecto=id_proyecto, estado_sprint=estadoSprint.EN_EJECUCION).exists()
        return Sprint.objects.filter(estado_sprint=estadoSprint.EN_EJECUCION).exists()
    
    def sprint_creado(id_proyecto):
        """
        Método para verificar si existe un sprint en planificación
        """
        # return Sprint.objects.filter(id_proyecto=id_proyecto, estado_sprint=estadoSprint.EN_PLANIFICACION).exists()
        return Sprint.objects.filter(estado_sprint=estadoSprint.EN_PLANIFICACION).exists()
    
