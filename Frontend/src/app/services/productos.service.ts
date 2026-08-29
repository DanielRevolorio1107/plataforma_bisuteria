import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface Producto {
  id_producto: number;
  id_categoria: number;
  codigo: string;
  nombre: string;
  descripcion: string | null;
  material: string | null;
  color: string | null;
  estilo: string | null;
  precio: number;
  imagen_url: string | null;
  activo: boolean;
  fecha_creacion: string;
}


export interface ProductoCreate {
  id_categoria: number;
  codigo: string;
  nombre: string;
  descripcion: string | null;
  material: string | null;
  color: string | null;
  estilo: string | null;
  precio: number;
  imagen_url: string | null;
}


@Injectable({
  providedIn: 'root'
})
export class ProductosService {

  private http = inject(HttpClient);

  private apiUrl =
    'http://127.0.0.1:8000/productos/';


  obtenerProductos(): Observable<Producto[]> {

    return this.http.get<Producto[]>(
      this.apiUrl
    );
  }


  obtenerProducto(
    id: number
  ): Observable<Producto> {

    return this.http.get<Producto>(
      `${this.apiUrl}${id}`
    );
  }


  obtenerTodosAdmin(): Observable<Producto[]> {

    return this.http.get<Producto[]>(
      `${this.apiUrl}admin/todos`
    );
  }


  crearProducto(
    producto: ProductoCreate
  ): Observable<Producto> {

    return this.http.post<Producto>(
      this.apiUrl,
      producto
    );
  }

}