/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pokergame;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

/**
 *
 * @author HowleR
 */
public class Deck 
{
    Random rg = new Random();

    public ArrayList<Card> buildDeck(ArrayList<Card> deck)
    {
        
        for(int i=0;i<13;i++)
        {           
              Card h = new Card();
              h.suit = 0;
              h.value = i;
              deck.add(h);            
        }
                        
        for(int i=0;i<13;i++)
        {
              Card d = new Card();
              d.suit = 1;
              d.value = i;
              deck.add(d);
        }
            
        for(int i=0;i<13;i++)
        {
              Card s = new Card();
              s.suit = 2;
              s.value = i;
              deck.add(s);
        }
            
        for(int i=0;i<13;i++)
        {
              Card c = new Card();
              c.suit = 3;
              c.value = i;
              deck.add(c);            
        }
        Collections.shuffle(deck); // built in Java method
        return deck;
    }
}








































