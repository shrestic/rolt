from rolt.common.utils import invalidate_cache

clear_preset_builds_cache = invalidate_cache(specific_key="preset_builds_list")
clear_service_list_cache = invalidate_cache(specific_key="service_list")
clear_showcase_list_cache = invalidate_cache(specific_key="showcase_list")
