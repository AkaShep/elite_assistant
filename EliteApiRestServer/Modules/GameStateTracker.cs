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

            _api.Events.On<GearStatusEvent>(e =>
            {
                State.IsLandingGearDown = e.Value;
                Console.WriteLine($"[GameState] Landing gear: {e.Value}");
            });

            _api.Events.On<LightsStatusEvent>(e =>
            {
                State.AreLightsOn = e.Value;
                Console.WriteLine($"[GameState] Lights: {e.Value}");
            });

            _api.Events.On<CargoScoopStatusEvent>(e =>
            {
                State.IsCargoScoopDeployed =e.Value;
                Console.WriteLine($"[GameState] Cargo scoop: {e.Value}");
            });

            _api.Events.On<HardpointsStatusEvent>(e =>
            {
                State.IsHardpointsDeployed = e.Value;
                Console.WriteLine($"[GameState] Hardpoints: {e.Value}");
            });


            _api.Events.On<DockedStatusEvent>(e =>
            {
                State.IsDocked = e.Value;
                Console.WriteLine($"[GameState] Docked: {e.Value}");
            });

            _api.Events.On<InMothershipStatusEvent>(e =>
            {
                State.InMothershipStatus = e.Value;
                Console.WriteLine($"[GameState] получил InMothershipEvent: {e.Value}");
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
