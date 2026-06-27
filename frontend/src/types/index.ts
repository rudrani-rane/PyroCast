export interface HealthResponse {
  status: "healthy" | "unhealthy";
  service: string;
  version: string;
  environment: string;
  timestamp: string;
}

export interface BoundingBox {
  minLongitude: number;
  minLatitude: number;
  maxLongitude: number;
  maxLatitude: number;
}
