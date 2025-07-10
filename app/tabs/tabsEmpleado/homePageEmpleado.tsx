import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { ActivityIndicator, Alert, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

const solicitudes = [
  { id: '1', documento: 'Vacaciones junio', supervisor: 'Carlos Ruiz', estado: 'aprobado', fecha: '2024-06-15' },
  { id: '2', documento: 'Licencia', supervisor: 'Carlos Ruiz', estado: 'pendiente', fecha: '2024-06-20' },
  { id: '3', documento: 'Cambio horario', supervisor: 'Maria Hernandez', estado: 'rechazado', fecha: '2024-06-22' },
  { id: '4', documento: 'Permiso especial', supervisor: 'Juan Soto', estado: 'aprobado', fecha: '2024-06-25' },
  { id: '5', documento: 'Licencia médica', supervisor: 'Carlos Ruiz', estado: 'pendiente', fecha: '2024-06-27' },
];

export default function HomePage() {
  const router = useRouter();
  const [solicitudes, setSolicitudes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8080/api/solicitudes')
      .then(res => res.json())
      .then(data => setSolicitudes(data))
      .catch(err => {
        Alert.alert('Error', 'No se pudieron cargar las solicitudes');
        console.error(err);
      })
      .finally(() => setLoading(false));
  }, []);

  const irADetalle = (solicitudId: string) => {
    console.log("redirecciona", solicitudId);
  };

  const renderRow = (item: any) => (
    <View style={styles.row} key={item.id}>
      <Text style={styles.cell}>{item.id}</Text>
      <Text style={styles.cell}>{item.titulo}</Text>
      <Text style={styles.cell}>{item.supervisor?.nombre || '-'}</Text>
      <Text style={styles.cell}>{item.estado || '-'}</Text>
      <Text style={styles.cell}>{item.fecha?.slice(0, 10) || '-'}</Text>
      <TouchableOpacity style={styles.button} onPress={() => irADetalle(item.id)}>
        <Text style={styles.buttonText}>Ver</Text>
      </TouchableOpacity>
    </View>
  );

  const renderTabla = (titulo: string, data: typeof solicitudes) => (
    <View style={styles.tableContainer}>
      <Text style={styles.subtitle}>{titulo}</Text>
      <View style={styles.headerRow}>
        <Text style={styles.headerCell}>#</Text>
        <Text style={styles.headerCell}>Solicitud</Text>
        <Text style={styles.headerCell}>Supervisor</Text>
        <Text style={styles.headerCell}>Estado</Text>
        <Text style={styles.headerCell}>Fecha</Text>
        <Text style={styles.headerCell}></Text>
      </View>
      {data.map(renderRow)}
    </View>
  );

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#4CAF50" />
      </View>
    );
  }

  const solicitudesAprobadas = solicitudes.filter(s => s.estado === 'aprobado');
  const solicitudesPendientes = solicitudes.filter(s => s.estado === 'pendiente');
  const solicitudesRechazadas = solicitudes.filter(s => s.estado === 'rechazado');

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Documentos Subidos</Text>
      {renderTabla('Solicitudes Aprobadas', solicitudesAprobadas)}
      {renderTabla('Solicitudes Pendientes', solicitudesPendientes)}
      {renderTabla('Solicitudes Rechazadas', solicitudesRechazadas)}
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
