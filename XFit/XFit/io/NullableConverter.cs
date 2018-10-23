using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

namespace XFit.io
{
    public class NullableConverter : JsonConverter
    {
        public override bool CanConvert(Type objectType)
            => objectType == typeof(string);

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
            => serializer.Deserialize<List<string>>(reader);

        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            var t = JToken.FromObject(value);
            if (t!=null)
            t.WriteTo(writer);
        }
    }
}
