using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

namespace XFit.io
{
    // Provides a mapping between a dictionary on the C# side and
    // a list of key-value tuples on the JSON side
    public class RelationConverter<T1,T2> : JsonConverter
    {
        public override bool CanConvert(Type objectType)
            => objectType == typeof(Dictionary<T1,T2>);

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            Dictionary<T1, T2> result = new Dictionary<T1, T2>();
            var raw = serializer.Deserialize<List<List<object>>>(reader);
            foreach (var elem in raw)
                result[(T1)elem[0]] = (T2)elem[1];
            return result;
        }

        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            var dict = value as Dictionary<T1, T2>;
            var list = new List<List<object>>();
            foreach (var key in dict.Keys)
                list.Add(new List<object> { key,dict[key]});
            JToken.FromObject(list).WriteTo(writer);
        }
    }
}
