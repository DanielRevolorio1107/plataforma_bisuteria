import { Injectable, computed, signal } from '@angular/core';

import { Producto } from './productos.service';


export interface ItemCarrito {
  producto: Producto;
  cantidad: number;
}


@Injectable({
  providedIn: 'root'
})
export class CarritoService {

  private itemsSignal = signal<ItemCarrito[]>([]);

  items = this.itemsSignal.asReadonly();

  cantidadTotal = computed(() =>
    this.itemsSignal().reduce(
      (total, item) => total + item.cantidad,
      0
    )
  );

  total = computed(() =>
    this.itemsSignal().reduce(
      (total, item) =>
        total + Number(item.producto.precio) * item.cantidad,
      0
    )
  );


  agregarProducto(producto: Producto): void {

    const items = [...this.itemsSignal()];

    const existente = items.find(
      item => item.producto.id_producto === producto.id_producto
    );

    if (existente) {
      existente.cantidad++;
    } else {
      items.push({
        producto,
        cantidad: 1
      });
    }

    this.itemsSignal.set(items);
  }


  aumentar(idProducto: number): void {

    const items = this.itemsSignal().map(item => {

      if (item.producto.id_producto === idProducto) {
        return {
          ...item,
          cantidad: item.cantidad + 1
        };
      }

      return item;
    });

    this.itemsSignal.set(items);
  }


  disminuir(idProducto: number): void {

    const items = this.itemsSignal()
      .map(item => {

        if (item.producto.id_producto === idProducto) {
          return {
            ...item,
            cantidad: item.cantidad - 1
          };
        }

        return item;
      })
      .filter(item => item.cantidad > 0);

    this.itemsSignal.set(items);
  }


  eliminar(idProducto: number): void {

    const items = this.itemsSignal().filter(
      item => item.producto.id_producto !== idProducto
    );

    this.itemsSignal.set(items);
  }


  vaciar(): void {
    this.itemsSignal.set([]);
  }
}