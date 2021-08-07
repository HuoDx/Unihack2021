Tech Specs
===

This document describes the technical specs of the project.

## 1. HTTP API

HTTP APIs are used for authentication and exchanging information that does not require real-time updates.

### 1.1 Register [POST]

Register an account.

#### Request
-   email, string: the email for this account.
-   password, string: the password.

#### Response
-   status, int: 0 - ok; 1 - error.
-   Sets the session token to cookie.

### 1.2 Login [POST]

Login to an account.

#### Request
-   email, string: the email registered.
-   password, string: the password.
-   next, string(url): the url when logged in successfully. Notice this url **MUST BE** safe, otherwise this field will be considered as null.

#### Response
-   Sets the session token to cookie.
-   Redirects to the URL in `next`.

### 1.3 Get Nearby Spots [GET]

Use a coordinate* to locate nearby Spots**.

*: the coordinate is encrypted by Baidu to satisfy legal requirements in China.

**: Spots, the place where help and resources are availiable. Technically, live and dynamic POIs. 

#### Request
-   lng, double: the longitude of the user's current position.
-   lat, double: the latitude of the user's current position.

#### Response
-   result, [SpotBriefInfo](#spotbriefinfo)[]:

##### `SpotBriefInfo` Object:
-   spot_uid, string: the UID for this spot. Users can subscribe to the spot via `socket.io` for real-time updates.
-   capcacity, int: how many people a spot can hold. Represented in symbol C in formulas.
-   availability, int: 
    This is computed at the backend by using `peopleArrived`(P), `peopleArriving`(G), and an algorithm will tell if you can expect room.
    - 0 (P + G < C): you can go to this spot.
    - 1 (P + G >= C, P < C): it's possible that there's still some room for you.
    - 2 (P >= C): Not availiable.





    