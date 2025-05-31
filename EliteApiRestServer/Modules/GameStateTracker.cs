using System;
using System.IO;
using System.Text.Json;
using System.Collections.Generic;
using System.Reflection;
using EliteAPI.Abstractions;
using EliteAPI.Abstractions.Events;

namespace EliteApiRestServer.Modules
{
    public class GameState
    {
        public Dictionary<string, Dictionary<string, object>> Events { get; set; } = new();
    }

    public class GameStateTracker
    {
        private readonly IEliteDangerousApi _api;
        private readonly string _saveFile = "gamestate.json";

        public GameState State { get; private set; }

        public GameStateTracker(IEliteDangerousApi api)
        {
            _api = api;
            State = LoadState();

            SetupSubscriptions();
        }

        private void SetupSubscriptions()
        {
            _api.Events.OnAny((e, context) =>
            {
                var eventType = e.GetType();
                var eventName = eventType.Name;

                var eventData = new Dictionary<string, object>();
                ExtractPropertiesRecursive(eventType, e, eventData, "");

                if (eventData.Count > 0)
                {
                    State.Events[eventName] = eventData;
                    Console.WriteLine($"[GameState] Updated {eventName}: {JsonSerializer.Serialize(eventData)}");

                    SaveState();
                }
            });
        }

        private void ExtractPropertiesRecursive(Type type, object obj, Dictionary<string, object> output, string prefix)
        {
            if (obj == null) return;

            foreach (var prop in type.GetProperties(BindingFlags.Public | BindingFlags.Instance))
            {
                var value = prop.GetValue(obj);
                if (value == null) continue;

                var propName = string.IsNullOrEmpty(prefix) ? prop.Name : $"{prefix}.{prop.Name}";
                var valueType = value.GetType();

                if (IsPrimitiveOrSimple(valueType))
                {
                    output[propName] = value;
                }
                else if (typeof(System.Collections.IEnumerable).IsAssignableFrom(valueType) && valueType != typeof(string))
                {
                    int index = 0;
                    foreach (var item in (System.Collections.IEnumerable)value)
                    {
                        ExtractPropertiesRecursive(item.GetType(), item, output, $"{propName}[{index}]");
                        index++;
                    }
                }
                else
                {
                    ExtractPropertiesRecursive(valueType, value, output, propName);
                }
            }
        }

        private static bool IsPrimitiveOrSimple(Type type)
        {
            return type.IsPrimitive ||
                   type.IsEnum ||
                   type == typeof(string) ||
                   type == typeof(decimal) ||
                   type == typeof(DateTime);
        }

        private GameState LoadState()
        {
            if (File.Exists(_saveFile))
            {
                try
                {
                    var json = File.ReadAllText(_saveFile);
                    var restored = JsonSerializer.Deserialize<GameState>(json);
                    Console.WriteLine("[GameState] Загружено сохранённое состояние");
                    return restored ?? new GameState();
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[GameState] Ошибка загрузки состояния: {ex.Message}");
                }
            }
            return new GameState();
        }

        private void SaveState()
        {
            try
            {
                var json = JsonSerializer.Serialize(State, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(_saveFile, json);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[GameState] Ошибка сохранения состояния: {ex.Message}");
            }
        }
    }
}
