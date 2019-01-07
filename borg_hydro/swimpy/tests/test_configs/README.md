# Description of the test configuration files

- *obj* number of objective functions
- *npr* number of parameter regions
- *gof* goodness of fit measures
- *npara* number parameters
- *nested* do we have nested objective functions in the configuration


| filename                  | nobj | npr | gof | npara | nested |  notes                         |
|---------------------------|------|-----|-----|-------|--------|--------------------------------|
|     ./01-config.json      | 2    | 1   | 1   |  6    |  F     |                                |
|     ./02-config.json      | 4    | 2   | 1   |  1    |  F     |                                |
|     ./03-config.json      | 2    | 1   | 2   |  1    |  F     | use different date format to set evaluation period |
|     ./04-config.json      | 3    | 1   | 1   |  1    |  T     | use different date format to set evaluation period |
|     ./05-config.json      | 1    | 1   | 1   |  3    |  F     | Fails to init                  |
|     ./06-config.json      | 2    | 4   | 2   |  6    |  F     |                                |
|     ./07-config.json      | 4    | 4   | 2   |  6    |  T     |                                |
|     ./08-config.json      | 1    | 1   | 1   |  1    |  F     | simplest setup                 |
|     ./09-config.json      | 1    | 3   | 1   |  2    |  F     | para regions not in sequence   |
|     ./10-config.json      | 4    | 4   | 2   |  6    |  T     | temporal aggregation           |
