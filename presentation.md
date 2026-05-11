# Presentation

Context

## Intro

Aujourd'hui, on est dans un tournant historique avec le développement fulgurant de l'IA.
De l'optimisation de [insérer un truc compliqué] à l'usage quotidien, l'IA s'impose comme un outil important.

De plus, l'apparition des voitures dites connectés sur les routes a

Les jamitons

La question qu'on va se poser dans cette étude est :

- L'intelligence artificielle va-t-elle permettre d'optimiser le trafic routier et, en particulier, prévenir l'apparition des jamitons ?

## L'apprentissage par renforcement

Le Q Learning est l'apprentissage par renforcement le plus simple et qui rentrant dans le cadre du programme sur les séries et les probabilités.
Ce dernier se base sur un tableau représentant tous les états possibles et la qualité associée à chaque action.

Or, on simule le trafic dans un milieu continu. Ainsi, il faut discrétiser l'espace des états. Cela résulte en une perte d'information montrant déjà une des faiblesses du Q Learning. Malgré cela, on arrivera tout de même à des résultats intéressants dans la suite de cette étude.

## Variation du système de récompense et conséquence sur les jamitons

1. ```python
   reward = (
     self.speed
   )
   ```

1. ```python
   reward = (
     self.speed -
     abs(self.speed - next.speed)
   )
   ```

1. ```python
   reward = (
     self.speed -
     abs(self.speed - avgSpeed) -
     abs(self.speed - next.speed)
   )
   ```

1. ```python
   reward = (
     self.speed -
     abs(self.speed - minSpeed) -
     abs(self.speed - next.speed)
   )
   ```

1. ```python
   reward = (
     newStateSelfSpeed
     * newStateDist
     / 100
   )
   ```

Choses à aborder :

- Modèle de Payne Whitnam
- Mesurer les jamitons
- Intro pareil que la MCOT

les fichiers json correspondent à la numérotation du dessus
