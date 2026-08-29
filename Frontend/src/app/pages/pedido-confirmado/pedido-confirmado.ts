import { Component } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

@Component({
  selector: 'app-pedido-confirmado',
  imports: [RouterLink],
  templateUrl: './pedido-confirmado.html',
  styleUrl: './pedido-confirmado.css'
})
export class PedidoConfirmado {

  idPedido: number;

  constructor(
    private route: ActivatedRoute
  ) {
    this.idPedido = Number(
      this.route.snapshot.paramMap.get('id')
    );
  }
}