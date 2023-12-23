export interface IDevice {
    device_id: string;
    name: string;
    status: string;
    x1: number;
    y1: number;
    x2: number;
    y2: number;
}
export interface IEventLog {
    event_id: number;
    device_id: string;
    timestamp: string;
    event_type: string;
    event_description: string;
}