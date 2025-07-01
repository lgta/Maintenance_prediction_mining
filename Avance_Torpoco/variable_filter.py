"""Dictionary with domain‑specific feature buckets."""
FEATURE_BUCKETS = {
    'feed': [
        'feed_rate_mean', 'feed_rate_std', 'feed_rate_min', 'feed_rate_max',
        'feed_rate_p95', 'feed_rate_cv'
    ],
    'speed': [
        'velocidad_rotacion_mean', 'velocidad_rotacion_std', 'velocidad_rotacion_min',
        'velocidad_rotacion_max', 'velocidad_rotacion_p95', 'velocidad_cv'
    ],
    'load': [
        'power_draw_mean', 'power_draw_std'
    ]
    # Add more based on domain knowledge
}