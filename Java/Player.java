/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pokergame;

/**
 *
 * @author HowleR
 */
public class Player 
{
    Card[] hand = new Card[5];
    String name;
    
    public Player(){}
    
    public void showHand()
    {
        for(Card c : hand)
        {
            System.out.println(c.toString());
        }
    }
}
