using EliteAPI.Abstractions;
using EliteAPI.Abstractions.Events;
using EliteAPI.Status.Ship.Events;
using EliteAPI.Status.Ship;
using EliteAPI.Events;
using System;

namespace EliteApiRestServer.Modules
{
    public class GameState
    {
        public bool IsLandingGearDown { get; set; }
        public bool AreLightsOn { get; set; }
        public bool IsCargoScoopDeployed { get; set; }
        public bool IsHardpointsDeployed { get; set; }
        public bool IsDocked { get; set; }
        public bool InMothershipStatus { get; set; }
        public bool UnderAttack { get; set; }
        public DateTime LastUnderAttackTime { get; set; }
        


        // Добавляй сюда любые новые поля по мере необходимости
    }

    public class GameStateTracker
    {
        private readonly IEliteDangerousApi _api;
        public GameState State { get; } = new();
        private readonly TimeSpan underAttackTimeout = TimeSpan.FromSeconds(10);

        public GameStateTracker(IEliteDangerousApi api)
        {
            _api = api;

            _api.Events.On<GearStatusEvent>((gear, ctx) =>
            {
                State.IsLandingGearDown = gear.Value;
                Console.WriteLine($"[GameState] Landing gear: {gear.Value}");
            });

            _api.Events.On<LightsStatusEvent>((lights, ctx) =>
            {
                State.AreLightsOn = lights.Value;
                Console.WriteLine($"[GameState] Lights: {lights.Value}");
            });

            _api.Events.On<CargoScoopStatusEvent>((scoop, ctx) =>
            {
                State.IsCargoScoopDeployed = scoop.Value;
                Console.WriteLine($"[GameState] Cargo scoop: {scoop.Value}");
            });

            _api.Events.On<HardpointsStatusEvent>((hardpoints, ctx) =>
            {
                State.IsHardpointsDeployed = hardpoints.Value;
                Console.WriteLine($"[GameState] Hardpoints: {hardpoints.Value}");
            });


            _api.Events.On<DockedStatusEvent>((docked, ctx) =>
            {
                State.IsDocked = docked.Value;
                Console.WriteLine($"[GameState] Docked: {docked.Value}");
            });

            _api.Events.On<InMothershipStatusEvent>((vehicle, ctx) =>
            {
                State.InMothershipStatus = vehicle.Value;
                Console.WriteLine($"[GameState] Vehicle status: {vehicle.Value}");
            });

            _api.Events.On<UnderAttackEvent>((attack, ctx) =>
            {
                State.UnderAttack = true;
                State.LastUnderAttackTime = DateTime.Now;
                Console.WriteLine("[GameState] Под атакой!");
            });

        }
        public bool IsUnderAttackActive()
        {
            if (!State.UnderAttack)
                return false;

            if ((DateTime.Now - State.LastUnderAttackTime) > underAttackTimeout)
            {
                State.UnderAttack = false;
                return false;
            }

            return true;
        }
    } 
}
