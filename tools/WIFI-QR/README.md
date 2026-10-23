# Wi-Fi QR Code

Single-file generator for Wi-Fi onboarding QR codes. Open `wlan-qr.html` in a
browser, enter SSID and PSK, print the cards. UI is German.

- Everything is computed in the browser. The PSK is never sent anywhere and
  never stored — no `localStorage`, gone when the tab is closed.
- Prints four cards per A4 sheet or one large card, and exports a 1024 px PNG.
- Handles the `\ ; , : "` escaping the `WIFI:` scheme requires, plus hidden
  SSIDs and open networks.
- The only remote script is the QR library from cdnjs, pinned with an SRI hash,
  so a swapped file on the CDN will not execute. Fonts come from Google Fonts.
  Once cached, the page works offline.

## Scheme

```
WIFI:T:WPA;S:<ssid>;P:<psk>;H:true;;
```

`T` is `WPA` (what scanners expect for WPA2 and WPA3-Personal alike), `WEP`, or
`nopass`. `H:true` only for a hidden SSID. iOS 11+ and Android 10+ read this
straight from the camera app.

## Notes

- The card prints the PSK in plain text by default, so people can type it in
  when a camera scan fails. Switch that off for anything but a guest network.
- A QR code is convenience, not a control: anyone who can photograph the card
  has the PSK. Guest networks belong on their own SSID and VLAN with client
  isolation, and the PSK should be rotated on a schedule.
