import sys
import json
sampleDict = {
    "price": sys.argv[1],
    "time": sys.argv[2]
}
jsonData = json.dumps(sampleDict)
print(jsonData)
