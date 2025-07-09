import { View, Text, StyleSheet, TouchableOpacity, FlatList } from 'react-native';
import { useRouter } from 'expo-router';

const empleados = [
  { id: '1', documento: 'Vacaciones junio', supervisor: 'Carlos Ruiz', estado: 'aprobado' },
  { id: '2', documento: 'Licencia', supervisor: 'Carlos Ruiz', estado: 'pendiente' },
  { id: '3', documento: 'Cambio horario', supervisor: 'Maria Hernandez', estado: 'rechazado' },
];

export default function VerDocs() {
  const router = useRouter();

  const irADetalle = (empleadoId: string) => {
    console.log("redirecciona", empleadoId);
    // router.push(...)
  };

  const renderItem = ({ item }: { item: typeof empleados[0] }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.id}</Text>
      <Text style={styles.cell}>{item.documento}</Text>
      <Text style={styles.cell}>{item.supervisor}</Text>
      <Text style={styles.cell}>{item.estado}</Text>
      <TouchableOpacity style={styles.button} onPress={() => irADetalle(item.id)}>
        <Text style={styles.buttonText}>Ver</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Documentos Subidos</Text>

      <View style={styles.headerRow}>
        <Text style={styles.headerCell}>numero</Text>
        <Text style={styles.headerCell}>Solicitud</Text>
        <Text style={styles.headerCell}>Supervisor</Text>
        <Text style={styles.headerCell}>Estado</Text>
        <Text style={styles.headerCell}> </Text>
      </View>

      <FlatList
        data={empleados}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        ItemSeparatorComponent={() => <View style={styles.separator} />}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingVertical: 24,
    paddingHorizontal: 16,
    backgroundColor: '#fff',
    alignItems: 'center',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center',
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 16,
    paddingHorizontal: 10,
  },
  headerCell: {
    flex: 1,
    fontWeight: 'bold',
    textAlign: 'left',
    fontSize: 14,
    paddingHorizontal: 50,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',    // alinea verticalmente al centro
    paddingVertical: 16,
    paddingHorizontal: 8,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    marginHorizontal: 8,
  },
  separator: {
    height: 20,   // más separación vertical entre filas
  },
  cell: {
    flex: 1,
    textAlign: 'center',
    fontSize: 14,
    marginHorizontal: 50,   // más espacio horizontal entre celdas
  },
  button: {
    backgroundColor: '#4CAF50',
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 6,
    alignSelf: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 14,
    textAlign: 'center',
  },
});
