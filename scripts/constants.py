JSbuiltInObj = ['__UNKNOWN',  ## Placeholder for unknown
                'infinity',
                'nan',
                'undefined',
                'null',
                'array',
                'boolean',  # Self added
                'string',
                'regexp',
                'number',
                'math',
                'date',
                'int8array',
                'uint8array',
                'uint8clampedarray',
                'int16array',
                'uint16array',
                'int32array',
                'uint32array',
                'float32array',
                'float64array']

words_to_ignore = ["__UNKNOWN__", "_UNKNOWN_"]

training_column_names = ["Function_Name", "Comment", "Return_Name", "Return_description",
                         "Parameter_description" ]

type_strings_mappings = {'arraytype':'array', 'array-type':'array','array-like': 'array', 'arraylike': 'array',
                         'functiontype':'function',
                         'integer':'number', r'\b(int)\b':'number', 'float':'number', 'double':'number', 'int':'number', 'long':'number'}

punctuation = """!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~"""

number_types = ["int","integer","float", "double", "uint", "uint32"]
boolean_types = ["bool", "boolean"]
none_types = ["null", "none", "undefined"]
array_types = ["ndarray"]
