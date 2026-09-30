import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from '../config/api.config';


export interface Inventario {
  id_inventario: number;
  id_producto: number;
  stock_actual: number;
  stock_minimo: number;
  fecha_actualizacion: string;
}

export interface InventarioUpdate {
  stock_actual: number;
  stock_minimo: number;
}

@Injectable({
  providedIn: 'root'
})
export class InventarioService {

  private http = inject(HttpClient);

  private apiUrl =
  `${API_URL}/inventario/`;


  obtenerInventario(): Observable<Inventario[]> {

    return this.http.get<Inventario[]>(
      this.apiUrl
    );
  }

  actualizarInventario(
  idProducto: number,
  datos: InventarioUpdate
): Observable<Inventario> {

  return this.http.put<Inventario>(
    `${this.apiUrl}${idProducto}`,
    datos
  );
}

}