using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

namespace XFit.io
{
    // Provides a mapping between a dictionary on the C# side and
    // a list of key-value tuples on the JSON side
    public class RelFlatStr3IntConverter : JsonConverter
    {
        public override bool CanConvert(Type objectType)
            => objectType == typeof(Dictionary<Tuple<string, string, string>, int>);

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            Dictionary<Tuple<string, string, string>, int> result = new Dictionary<Tuple<string, string, string>, int>();
            var raw = serializer.Deserialize<List<object>>(reader);
            bool name = true;
            Tuple<string, string, string> key = new Tuple<string, string, string>("", "", "");
            foreach (var elem in raw)
            {
                if (name)
                {
                    JArray arr = elem as JArray;
                    key = new Tuple<string, string, string>((string)arr[0], (string)arr[1], (string)arr[2]);
                }
                else
                    result[key] = (int)(long)elem;
                name = !name;
            }
            return result;
        }

        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            var dict = value as Dictionary<Tuple<string, string, string>, int>;
            var flat = new Dictionary<string, int>();
            // legacy:
            foreach (var key in dict.Keys)
                flat[$"{key.Item1}/{key.Item2}/{key.Item3}"] = dict[key];
            JToken.FromObject(flat).WriteTo(writer);
        }
    }
}
