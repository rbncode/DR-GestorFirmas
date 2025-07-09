// app/_layout.tsx
import { Stack, usePathname } from 'expo-router';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';

export default function RootLayout() {
  const pathname = usePathname();
  const router = useRouter();
  //Ocultar navbar en login
  const hideNavbar = pathname === '/login';
    const volverHome = () => {
        router.replace('/tabs/tabsEmpleado/homePageEmpleado');
    };

    const SubirSolicitud = () => {
        router.replace('/tabs/tabsEmpleado/UploadFileEmpleado');
    };
    const VerSolicitudes = () => {
        router.replace('/tabs/tabsEmpleado/verDocsEmpleado');
    };
    const cerrarSesion = () => {
        router.replace('/login');
    };

    const VerPendientes = () => {
        router.replace('/tabs/tabsSupervisor/verPendientesSupervisor');
    };

    const HomePAgeSupervisor = () => {
        router.replace('/tabs/tabsSupervisor/homePageSupervisor');
    };

    const HomeHR = () => {
        router.replace('/tabs/tabsRH/homePageRH');
    };

    const historial = () => {
        router.replace('/tabs/tabsRH/historyFiles');
    };

  return (
    <View style={{ flex: 1 }}>
      {!hideNavbar && (
        <View style={styles.navbar}>
            <TouchableOpacity style={styles.button} onPress={volverHome}>
                <Text style={styles.buttonText}>Simple Firma</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={SubirSolicitud}>
                <Text style={styles.buttonText}>Subir Solicitud</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={VerSolicitudes}>
                <Text style={styles.buttonText}>Ver mis solicitudes</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={VerPendientes}>
                <Text style={styles.buttonText}>Ver mis pendientes</Text>
            </TouchableOpacity>
             <TouchableOpacity style={styles.button} onPress={historial}>
                <Text style={styles.buttonText}>Historial</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={cerrarSesion}>
                <Text style={styles.buttonText}>Cerrrar Sesión</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={HomePAgeSupervisor}>
                <Text style={styles.buttonText}>Cambiar Supervisor</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={HomeHR}>
                <Text style={styles.buttonText}>cambiar hr </Text>
            </TouchableOpacity>
        </View>
      )}
      <Stack />
    </View>
  );
}

const styles = StyleSheet.create({
  navbar: {
    backgroundColor: '#4CAF50',
    height: 60,
    paddingHorizontal: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  navTitle: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  navButton: {
    color: '#fff',
    fontSize: 16,
  },
  button: {
    backgroundColor: '#4CAF50',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});
