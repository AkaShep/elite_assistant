using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using EliteAPI.Abstractions;
using EliteAPI.Abstractions.Events.Status;
using EliteAPI.Events.Status;

namespace EliteApiRestServer.Modules
{
    public class GameState
    {
        public bool IsLandingGearDown { get; set; }
        public bool AreLightsOn { get; set; }
        public bool IsCargoScoopDeployed { get; set; }
        public bool IsHardpointsDeployed { get; set; }
        public bool IsDocked { get; set; }
        public bool IsInMothership { get; set; }
        public bool UnderAttack { get; set; }
        public DateTime LastUnderAttackTime { get; set; }
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
            _api.Events.On<GearStatusEvent>(e =>
            {
                State.IsLandingGearDown = e.Value;
                SaveState();
                Console.WriteLine($"[GameState] Landing gear: {e.Value}");
            });

            _api.Events.On<LightsStatusEvent>(e =>
            {
                State.AreLightsOn = e.Value;
                SaveState();
                Console.WriteLine($"[GameState] Lights: {e.Value}");
            });

            _api.Events.On<CargoScoopStatusEvent>(e =>
            {
                State.IsCargoScoopDeployed = e.Value;
                SaveState();
                Console.WriteLine($"[GameState] Cargo scoop: {e.Value}");
            });

            _api.Events.On<HardpointsStatusEvent>(e =>
            {
                State.IsHardpointsDeployed = e.Value;
                SaveState();
                Console.WriteLine($"[GameState] Hardpoints: {e.Value}");
            });

            _api.Events.On<DockedStatusEvent>(e =>
            {
                State.IsDocked = e.Value;
                SaveState();
                Console.WriteLine($"[GameState] Docked: {e.Value}");
            });

            _api.Events.On<InMothershipEvent>(e =>
            {
                State.IsInMothership = e.Value;
                SaveState();
                Console.WriteLine($"[GameState] In mothership: {e.Value}");
            });

            _api.Events.On<UnderAttackEvent>(e =>
            {
                State.UnderAttack = e.Value;
                if (underAttack.Value)
                {
                    State.LastUnderAttackTime = DateTime.UtcNow;
                }
                SaveState();
                Console.WriteLine($"[GameState] Under attack: {e.Value}");
            });
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
