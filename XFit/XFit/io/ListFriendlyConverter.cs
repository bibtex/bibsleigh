using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;

namespace XFit.io
{
    public class ListFriendlyConverter : JsonConverter
    {
        public override bool CanConvert(Type objectType)
            => objectType == typeof(string)
            || objectType == typeof(List<string>);

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            if (reader.Value is string vs)
                return new List<string> { vs };
            else if (reader.Value is int vi)
                return new List<string> { vi.ToString() };
            else if (reader.Value is long vl)
                return new List<string> { vl.ToString() };
            else
                return serializer.Deserialize<List<string>>(reader);
        }

        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            var t = JToken.FromObject(value);
            if (t is JArray ta && ta.Count == 1)
                ta[0].WriteTo(writer);
            else
                t.WriteTo(writer);
        }
    }
}
