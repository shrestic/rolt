from rolt.common.utils import invalidate_cache

clear_keycap_cache = invalidate_cache(prefix="keycap_list:")
clear_kit_cache = invalidate_cache(prefix="kit_list:")
clear_switch_cache = invalidate_cache(prefix="switch_list:")
