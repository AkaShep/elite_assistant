// Program.cs
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using EliteAPI;
using EliteAPI.Abstractions.Events;
using EliteAPI.Events;
using EliteAPI.Abstractions;
using EliteAPI.Abstractions.Bindings;
using EliteAPI.Abstractions.Bindings.Models;
using EliteAPI.Status;
using EliteAPI.Status.Ship;
using EliteAPI.Status.Ship.Events;
using System.Collections.Concurrent;
using EliteApiRestServer.Modules;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Очередь последних 100 событий
var eventQueue = new ConcurrentQueue<IEvent>();

// EliteAPI инициализация
var host = Host.CreateDefaultBuilder()
    .ConfigureServices(s =>
    {
        s.AddEliteApi();
        
    })
    .Build();


var api = host.Services.GetRequiredService<IEliteDangerousApi>();


await api.StartAsync();

//Сюда вписывать подключаемые модули
var gameStateTracker = new GameStateTracker(api);

// Маршруты REST API
app.MapGet("/status", () => new { status = "EliteAPI запущен" });
app.MapGet("/ship-status", () => Results.Json(gameStateTracker.State));
app.MapGet("/bindings", () =>
{
    var result = new Dictionary<string, string>();

    foreach (KeyBinding key in Enum.GetValues(typeof(KeyBinding)))
    {
        try
        {
            var binding = api.Bindings[key];

            var primary = binding.Primary;
            if (primary == null)
            {
                result[key.ToString()] = "not set";
                continue;
            }

            var primaryKey = primary.Value.Key ?? "not set";
            var modifiers = primary.Value.Modifiers;

            string combined;

            if (modifiers != null && modifiers.Any())
            {
                var modifierNames = string.Join("+", modifiers.Select(m => m.Key));
                combined = $"{modifierNames}+{primaryKey}";
            }
            else
            {
                combined = primaryKey;
            }

            result[key.ToString()] = combined;
        }
        catch
        {
            result[key.ToString()] = "not set";
        }
    }

    return Results.Json(result);
});
app.MapGet("/last-event", () =>
{
    if (eventQueue.TryPeek(out var lastEvent))
    {
        return Results.Json(lastEvent);
    }
    return Results.NotFound("Нет событий");
});

app.MapGet("/events", (int count) =>
{
    var events = eventQueue.ToArray().Reverse().Take(count);
    return Results.Json(events);
});

app.MapGet("/", () => "EliteAPI REST сервер запущен");

app.Run("http://localhost:5000");
