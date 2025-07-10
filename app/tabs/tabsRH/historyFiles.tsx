import { ScrollView, View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';

// solicitudes ahora con campo "empleado"
const solicitudes = [
  { id: '1', documento: 'Vacaciones junio', empleado: 'Pedro Pérez', supervisor: 'Carlos Ruiz', estado: 'rechazado', fecha: '2024-06-15', recursosHumanos:'Juan Lopez' },
  { id: '2', documento: 'Licencia', empleado: 'Pedro Pérez', supervisor: 'Carlos Ruiz', estado: 'rechazado', fecha: '2024-06-20', recursosHumanos:'Pedro Perez' },
  { id: '3', documento: 'Cambio horario', empleado: 'Maria Hernandez', supervisor: 'Carlos Ruiz', estado: 'aprobado', fecha: '2024-06-22', recursosHumanos:'Juan Lopez' },
  { id: '4', documento: 'Permiso especial', empleado: 'Carlos Ruiz', supervisor: 'Juan Soto', estado: 'aprobado', fecha: '2024-06-25', recursosHumanos:'Juana Perez' },
  { id: '5', documento: 'Licencia médica', empleado: 'Carlos Ruiz', supervisor: 'Juan Soto', estado: 'aprobado', fecha: '2024-06-27', recursosHumanos:'Mario González' },
];

// supervisor logueado
const supervisorActual = "Carlos Ruiz";

export default function HomePageSupervisor() {
  const router = useRouter();

  const irADetalleRevision = (solicitudId: string) => {
    //router.push(`/tabs/tabsRH/revisarSolicitud?id=${solicitudId}`);
    router.replace('/tabs/tabsRH/revisionFileRH');
  };

  const irADetallePropia = (solicitudId: string) => {
    //router.push(`/tabs/tabSupervisor/verMiSolicitud?id=${solicitudId}`);
  };

  const renderRowPropia = (item: typeof solicitudes[0]) => (
    <View style={styles.row} key={item.id}>
      <Text style={styles.cell}>{item.id}</Text>
      <Text style={styles.cell}>{item.documento}</Text>
      <Text style={styles.cell}>{item.supervisor}</Text>
        <Text style={styles.cell}>{item.recursosHumanos}</Text>
        <Text style={styles.cell}>{item.fecha}</Text>
        <Text style={styles.cell}>{item.estado}</Text>
      <TouchableOpacity style={styles.button} onPress={() => irADetallePropia(item.id)}>
        <Text style={styles.buttonText}>Ver</Text>
      </TouchableOpacity>
    </View>
  );

  // solicitudes pendientes que tiene que revisar (supervisa a otros)
  const solicitudesPendientesRevision = solicitudes.filter(
    s => s.estado === 'pendiente' && s.supervisor === supervisorActual
  );

  
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Historial de Solicitudes</Text>

      {/* Solicitudes propias */}
      <View style={styles.tableContainer}>
        <Text style={styles.subtitle}>Mis Solicitudes</Text>
        <View style={styles.headerRow}>
            <Text style={styles.headerCell}></Text>
          <Text style={styles.headerCell}>id</Text>
          <Text style={styles.headerCell}>Solicitud</Text>
          <Text style={styles.headerCell}>Supervisor</Text>
          <Text style={styles.headerCell}>Recursos Humanos</Text>
          <Text style={styles.headerCell}>fecha</Text>
          <Text style={styles.headerCell}>estado</Text>
        </View>
        {solicitudes.map(renderRowPropia)}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingVertical: 24,
    paddingHorizontal: 16,
    backgroundColor: '#fff',
  },
  tableContainer: {
    marginBottom: 32,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    textAlign: 'center',
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 8,
    paddingHorizontal: 10,
  },
  headerCell: {
    flex: 1,
    fontWeight: 'bold',
    textAlign: 'left',
    fontSize: 14,
    paddingHorizontal: 4,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 8,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    marginVertical: 6,
  },
  cell: {
    flex: 1,
    textAlign: 'center',
    fontSize: 14,
    marginHorizontal: 4,
  },
  button: {
    backgroundColor: '#4CAF50',
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 14,
  },
});
