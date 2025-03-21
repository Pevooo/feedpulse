export interface RefreshToken {
    userName: string;
    token: string;
    expireat: string; // ISO 8601 date string; could use Date if you parse it
}