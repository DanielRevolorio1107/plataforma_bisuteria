import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from '../config/api.config';


export interface UploadResponse {
  imagen_url: string;
}


@Injectable({
  providedIn: 'root'
})
export class UploadsService {

  private http = inject(HttpClient);

  private apiUrl =
  `${API_URL}/uploads/producto`;


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