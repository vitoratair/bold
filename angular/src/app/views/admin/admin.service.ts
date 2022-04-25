import { HttpClient, HttpErrorResponse, HttpEventType} from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { catchError, retry } from "rxjs/operators";
import Swal from "sweetalert2";
import { map } from  'rxjs/operators';


@Injectable()
export class AdminService {
    private token = "Bearer 1PgxQwoSV3HHuR3eSuM6YLDxVB3QBU";

    constructor(private http: HttpClient) {}

    getItems(url: string) {
        const headers = {
            "Content-Type": "application/json",
            Authorization: this.token,
        };

        return this.http
            .get<any>(url, { headers })
            .pipe(catchError(this.handleError));
    }


    private handleError(error: HttpErrorResponse) {
        if (error.error instanceof ErrorEvent) {
            // A client-side or network error occurred. Handle it accordingly.
            console.error("An error occurred:", error.error.message);
        } else {
            // The backend returned an unsuccessful response code.
            // The response body may contain clues as to what went wrong.
            console.error(
                `Backend returned code ${error.status}, ` +
                    `body was: ${error.error}`
            );
        }
        // Return an observable with a user-facing error message.
        return throwError(error);
    }


    deleteItem(url: string) {
        const headers = {
            "Content-Type": "application/json",
            Authorization: this.token,
        };

        return this.http
            .delete<any>(url, { headers })
            .pipe(catchError(this.handleError));
    }




}
