import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface Categoria {
  id_categoria: number;
  nombre: string;
  descripcion: string | null;
  activo: boolean;
  fecha_creacion: string;
}


export interface CategoriaCreate {
  nombre: string;
  descripcion: string | null;
}

export interface CategoriaUpdate {
  nombre: string;
  descripcion: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class CategoriasService {

  private http = inject(HttpClient);

  private apiUrl =
    'http://127.0.0.1:8000/categorias/';


  obtenerCategorias(): Observable<Categoria[]> {

    return this.http.get<Categoria[]>(
      this.apiUrl
    );
  }


  obtenerTodasAdmin(): Observable<Categoria[]> {

    return this.http.get<Categoria[]>(
      `${this.apiUrl}admin/todas`
    );
  }


  crearCategoria(
    categoria: CategoriaCreate
  ): Observable<Categoria> {

    return this.http.post<Categoria>(
      this.apiUrl,
      categoria
    );
  }


  desactivarCategoria(
    idCategoria: number
  ): Observable<Categoria> {

    return this.http.delete<Categoria>(
      `${this.apiUrl}${idCategoria}`
    );
  }


  activarCategoria(
    idCategoria: number
  ): Observable<Categoria> {

    return this.http.patch<Categoria>(
      `${this.apiUrl}${idCategoria}/activar`,
      {}
    );
  }

  actualizarCategoria(
  idCategoria: number,
  categoria: CategoriaUpdate
): Observable<Categoria> {

  return this.http.patch<Categoria>(
    `${this.apiUrl}${idCategoria}`,
    categoria
  );
}
  
}