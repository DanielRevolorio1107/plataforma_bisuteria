import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface PedidoCreate {
  nombre_cliente: string;
  telefono: string;
  direccion_entrega: string;
  observaciones: string | null;

  productos: {
    id_producto: number;
    cantidad: number;
  }[];
}


export interface PedidoResponse {
  id_pedido: number;
  nombre_cliente: string;
  telefono: string;
  direccion_entrega: string;
  observaciones: string | null;
  estado: string;
  total: number;
  fecha_pedido: string;
}


export interface DetallePedidoResponse {
  id_detalle: number;
  id_pedido: number;
  id_producto: number;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
}


export interface PedidoDetalleResponse {
  id_pedido: number;
  nombre_cliente: string;
  telefono: string;
  direccion_entrega: string;
  observaciones: string | null;
  estado: string;
  total: number;
  fecha_pedido: string;
  detalles: DetallePedidoResponse[];
}


export interface PedidoEstadoUpdate {
  estado: string;
}


@Injectable({
  providedIn: 'root'
})
export class PedidosService {

  private http = inject(HttpClient);

  private apiUrl =
    'http://127.0.0.1:8000/pedidos/';


  crearPedido(
    pedido: PedidoCreate
  ): Observable<PedidoResponse> {

    return this.http.post<PedidoResponse>(
      this.apiUrl,
      pedido
    );
  }


  obtenerPedidos(): Observable<PedidoResponse[]> {

    return this.http.get<PedidoResponse[]>(
      this.apiUrl
    );
  }


  obtenerPedido(
    idPedido: number
  ): Observable<PedidoDetalleResponse> {

    return this.http.get<PedidoDetalleResponse>(
      `${this.apiUrl}${idPedido}`
    );
  }


  actualizarEstado(
    idPedido: number,
    estado: string
  ): Observable<PedidoResponse> {

    return this.http.patch<PedidoResponse>(
      `${this.apiUrl}${idPedido}/estado`,
      {
        estado: estado
      }
    );
  }

}