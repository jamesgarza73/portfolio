/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pokergame;

import java.util.ArrayList;

/**
 *
 * @author HowleR
 */
public class PokerGame 
{

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) 
    {
        
        ArrayList<Card> cards = new ArrayList<>();
        Deck deck = new Deck();
        cards = deck.buildDeck(cards);
        for(int i = 0;i<cards.size();i++)
        {
            System.out.println(cards.get(i).toString());
        }
    }
    
}
    
