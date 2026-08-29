import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  Producto,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-admin-productos',
  imports: [RouterLink],
  templateUrl: './admin-productos.html',
  styleUrl: './admin-productos.css'
})
export class AdminProductos implements OnInit {

  productos = signal<Producto[]>([]);
  cargando = signal(true);
  error = signal('');


  constructor(
    private productosService: ProductosService
  ) {}


  ngOnInit(): void {

    this.productosService.obtenerTodosAdmin().subscribe({

      next: (productos) => {
        this.productos.set(productos);
        this.cargando.set(false);
      },

      error: () => {
        this.error.set(
          'No se pudieron cargar los productos'
        );

        this.cargando.set(false);
      }

    });
  }

}