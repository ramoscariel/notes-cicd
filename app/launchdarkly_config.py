import os
import ldclient
from ldclient.config import Config
from ldclient import Context

# Configuración de LaunchDarkly
LAUNCHDARKLY_SDK_KEY = os.getenv("LAUNCHDARKLY_SDK_KEY", "")

# Inicializar el cliente de LaunchDarkly
def initialize_launchdarkly():
    if not LAUNCHDARKLY_SDK_KEY:
        print("WARNING: LaunchDarkly SDK key not found. Feature flags will be disabled.")
        return None

    ldclient.set_config(Config(LAUNCHDARKLY_SDK_KEY))
    client = ldclient.get()

    if client.is_initialized():
        print("LaunchDarkly initialized successfully")
    else:
        print("ERROR: LaunchDarkly failed to initialize")

    return client

# Cliente global de LaunchDarkly
ld_client = initialize_launchdarkly()

def get_feature_flag(flag_key: str, user_key: str = "anonymous", default_value: bool = False) -> bool:
    """
    Obtiene el valor de un feature flag de LaunchDarkly

    Args:
        flag_key: Nombre del feature flag
        user_key: Identificador del usuario (default: "anonymous")
        default_value: Valor por defecto si el flag no existe (default: False)

    Returns:
        bool: Valor del feature flag
    """
    if not ld_client:
        return default_value

    context = Context.builder(user_key).build()
    return ld_client.variation(flag_key, context, default_value)

def close_launchdarkly():
    """Cierra la conexión con LaunchDarkly"""
    if ld_client:
        ld_client.close()
