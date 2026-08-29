import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { CarritoService } from '../../services/carrito.service';


@Component({
  selector: 'app-carrito',
  imports: [RouterLink],
  templateUrl: './carrito.html',
  styleUrl: './carrito.css'
})
export class Carrito {

  constructor(
    public carritoService: CarritoService
  ) {}


  aumentar(idProducto: number): void {
    this.carritoService.aumentar(idProducto);
  }


  disminuir(idProducto: number): void {
    this.carritoService.disminuir(idProducto);
  }


  eliminar(idProducto: number): void {
    this.carritoService.eliminar(idProducto);
  }


  vaciar(): void {
    this.carritoService.vaciar();
  }
}