using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

namespace XFit.io
{
    // Provides a mapping between a dictionary on the C# side and
    // a list of key-value tuples on the JSON side
    public class RelStrIntConverter : JsonConverter
    {
        public override bool CanConvert(Type objectType)
            => objectType == typeof(Dictionary<string, int>);

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            Dictionary<string, int> result = new Dictionary<string, int>();
            var raw = serializer.Deserialize<List<List<object>>>(reader);
            foreach (var elem in raw)
                result[(string)elem[0]] = (int)(long)elem[1];
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
