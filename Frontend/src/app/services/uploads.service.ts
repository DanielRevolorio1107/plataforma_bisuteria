import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface UploadResponse {
  imagen_url: string;
}


@Injectable({
  providedIn: 'root'
})
export class UploadsService {

  private http = inject(HttpClient);

  private apiUrl =
    'http://127.0.0.1:8000/uploads/producto';


  subirImagen(
    archivo: File
  ): Observable<UploadResponse> {

    const formulario = new FormData();

    formulario.append(
      'archivo',
      archivo
    );


    return this.http.post<UploadResponse>(
      this.apiUrl,
      formulario
    );
  }

}