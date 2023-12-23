
import { setToastMessage } from "~/store";

export const statusToastHandler = (status: number, sucess: string|null) => {

    let message = sucess

    if (status === 404) { message = ("Device not found");}
    else if (status === 400) { message = ("Bad request");}
    else if (status === 401) { message = ("Unauthorized");}
    else if (status === 403) { message = ("Forbidden");}
    else if (status === 405) { message = ("Method not allowed");}
    else if (status === 406) { message = ("Not acceptable");}
    else if (status === 409) { message = ("Conflict");}
    else if (status === 415) { message = ("Unsupported media type");}
    else if (status === 422) { message = ("Unprocessable entity");}
    else if (status === 429) { message = ("Too many requests");}
    else if (status === 500) { message = ("Internal server error");}

    if (message !== null) { setToastMessage(message);}
}