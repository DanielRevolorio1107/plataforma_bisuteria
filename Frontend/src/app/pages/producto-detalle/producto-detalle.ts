import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { CarritoService } from '../../services/carrito.service';

import {
  Producto,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-producto-detalle',
  imports: [],
  templateUrl: './producto-detalle.html',
  styleUrl: './producto-detalle.css'
})
export class ProductoDetalle implements OnInit {

  producto = signal<Producto | null>(null);
  cargando = signal(true);
  error = signal('');

  constructor(
    private route: ActivatedRoute,
    private productosService: ProductosService,
    private carritoService: CarritoService
  ) {}


  ngOnInit(): void {

    const id = Number(
      this.route.snapshot.paramMap.get('id')
    );

    this.productosService.obtenerProducto(id).subscribe({

      next: (producto) => {
        this.producto.set(producto);
        this.cargando.set(false);
      },

      error: () => {
        this.error.set(
          'No se pudo cargar el producto'
        );

        this.cargando.set(false);
      }

    });
  }


  agregarAlCarrito(producto: Producto): void {
    this.carritoService.agregarProducto(producto);
  }

}