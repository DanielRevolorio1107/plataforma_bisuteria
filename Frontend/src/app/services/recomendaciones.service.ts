import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Producto } from './productos.service';
import { API_URL } from '../config/api.config';


export interface RecomendacionResultado {
  producto: Producto;
  puntuacion: number;
}


@Injectable({
  providedIn: 'root'
})
export class RecomendacionesService {

  private http = inject(HttpClient);

  private apiUrl =
  `${API_URL}/recomendaciones/`;


  obtenerRecomendaciones(
    idProducto: number
  ): Observable<RecomendacionResultado[]> {

    return this.http.get<RecomendacionResultado[]>(
      `${this.apiUrl}${idProducto}`,
      {
        params: {
          limite: 4
        }
      }
    );
  }

}