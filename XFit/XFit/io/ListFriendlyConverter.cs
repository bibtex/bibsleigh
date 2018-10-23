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
            try
            {
                var r = serializer.Deserialize<string>(reader);
                return new List<string> { r };
            }
            catch
            {
                return serializer.Deserialize<List<string>>(reader);
            }
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
