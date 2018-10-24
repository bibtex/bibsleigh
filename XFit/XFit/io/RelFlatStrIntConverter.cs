using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

namespace XFit.io
{
    // Provides a mapping between a dictionary on the C# side and
    // a list of key-value tuples on the JSON side
    public class RelFlatStrIntConverter : JsonConverter
    {
        public override bool CanConvert(Type objectType)
            => objectType == typeof(Dictionary<string, int>);

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            Dictionary<string, int> result = new Dictionary<string, int>();
            var raw = serializer.Deserialize<List<object>>(reader);
            bool name = true;
            string key = "";
            foreach (var elem in raw)
            {
                if (name)
                    key = (string)elem;
                else
                    result[key] = (int)(long)elem;
                name = !name;
            }
            return result;
        }

        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            var dict = value as Dictionary<string, int>;
            JToken.FromObject(dict).WriteTo(writer);
            return;
            // legacy:
            var list = new List<List<object>>();
            foreach (var key in dict.Keys)
                list.Add(new List<object> { key, (long)dict[key] });
            JToken.FromObject(list).WriteTo(writer);
        }
    }
}
