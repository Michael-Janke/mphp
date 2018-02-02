algorithms = {
    'getPCA': {
        "parameters": {
            "n_components": {
                "name": "#Components",
                "default": 3
            },
            "n_features_per_component": {
                "name": "#Features per component",
                "default": 10
            }
        },
        "name": "PCA"
    },
    'getDecisionTreeFeatures': {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10
            }
        },
        "name": "Decision Tree"
    },
    'getNormalizedFeaturesE': {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10

            },
            "n": {
                "name": "#Considered features",
                "default": 5000

            }
        },
        "name": "Feature Selection Normalization:Exclude"
    },
    'getNormalizedFeaturesS': {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10

            },
            "n": {
                "name": "#Considered features",
                "default": 5000

            }
        },
        "name": "Feature Selection Normalization:Substract"
    },
    "getFeatures": {
        "parameters": {
            "k": {
                "name": "#Features",
                "default": 10

            }
        },
        "name": "Feature Selection"
    },
    "getFeaturesBySFS": {
        "name": "Sequential Forward Selection (normalized)",
        "parameters": {}
    }
}
