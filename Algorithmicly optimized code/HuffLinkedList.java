/*
 * LinkedList.java
 *
 * Version:
 *     1
 *
 * Revisions:
 *     Add Node Class
 *     Add function methods from Storage
 *     Work on method implementation
 *     Add commenting
 *     Change functionality to work with Comparable
 *     Update commenting
 *
 */



/**
 * LinkedList stores comparables in a
 * linked list storage. It extends
 * StorageImplementation and implements
 * StorageInterface.
 *
 * @author      Luke Batchelder
 * @author      Jessica Diehl
 */
public class HuffLinkedList <T extends Comparable> extends HuffStorageImplementation {
    Node head;

    /**
     * Node class holds one data element and the
     * node next in the linked list.
     *
     * @author      Luke Batchelder
     * @author      Jessica Diehl
     */
    class Node {
        Comparable data;  //data used for storing comparable
        //Integer oc; //occurances of character
        String ch; //character for node
        Node next; //next node
        Node left; //left node
        Node right; //right node

        //constructor for Integer, String, left, right
        Node ()
        {
            data = "";
            ch = "";
            next = null;

            left = null;
            right = null;
        }
        //constructor for Integer, String, left, right
        Node (Comparable o, String c, Node l, Node r)
        {
            data = o;
            ch = c;
            next = null;

            left = l;
            right = r;
        }

        //constructor for Integer and String
        Node (Comparable o, String c)
        {
            data = o;
            ch = c;
            next = null;

            left = null;
            right = null;
        }

        //constructor for Comparable
        Node (Comparable e)
        {
            data = e;
            ch = "";
            next = null;
        }
    }

    /**
     * Loads an entire line into the linked list
     * by first checking that the item doesn't already
     * occur in the linked list. If the item doesn't
     * occur, it is added. If the item does occur,
     * the character count is incremented by one.
     *
     * @param       line    String to add to the linked list
     *
     * @return              None
     */

    public void ingestLine(String line) {
        int index = 0;
        String c = "";
        Integer d = 0;
        //loop through the line
        for(index = 0; index < line.length(); index++) {
            //get the next character in the line
            c = c.valueOf(line.charAt(index));

            //if the character exists in the list,
            //increment the integer occurrance value
            if(this.containsCh(c)) {
                d = (Integer)this.get(this.indexOfCh(c));
                d = d + 1;
                this.set(this.indexOfCh(c), d, c);
            } else {
                //the character doesn't exist in the
                //list, add this as a new node
                //with an occurrence value of 1
                this.addCh(c);
            }
        }
    }

    /**
     * Appends the specified element to the end of this list
     * along with the string character
     *
     * @param       data    int to add to the linked list
     *
     * @return              True if the element is added
     */
    public boolean addCh(String ch) {
        //create new node using a count and character (String)
        Node newNode = new Node(1,ch);
        newNode.next = null;  //node has no next node

        if(head == null)
        {
            //there is no head node so set this node
            //to be the head node
            head = newNode;
        } else
        {
            //reach the end of the list and insert
            Node lastNode = head;
            //increment through nodes until reached end
            while(lastNode.next != null) {
                lastNode = lastNode.next;
            }

            // Insert the new node at the end
            lastNode.next = newNode;
        }

        size++;

        return true;
    }



    /**
     * Appends the specified element to the end of this list
     * along with the string character
     *
     * @param       data    integer to add to the linked list
     * @param 		ch		string character to add to the list
     *
     * @return              True if the element is added
     */
    public boolean addCh(Comparable data, String ch) {
        //create new node using given data and character (String)
        Node newNode = new Node(data,ch);
        newNode.next = null;  //node has no next node

        if(head == null)
        {
            //there is no head node so set this node
            //to be the head node
            head = newNode;
        } else
        {
            //reach the end of the list and insert
            Node lastNode = head;
            //increment through nodes until reached end
            while(lastNode.next != null) {
                lastNode = lastNode.next;
            }

            // Insert the new node at the end
            lastNode.next = newNode;
        }

        size++;

        return true;
    }


    /**
     * Appends the specified element to the end of this list
     * along with the string character
     *
     * @param       data    integer to add to the linked list
     * @param 		ch		string character to add to the list
     *
     * @return              True if the element is added
     */
    public boolean addBNode(Comparable data, String ch,
                            Object left, Object right) {
        //create new node using given data and character (String)
        Node newNode = new Node(data,ch,(Node)left,(Node)right);
        newNode.next = null;  //node has no next node

        if(head == null)
        {
            //there is no head node so set this node
            //to be the head node
            head = newNode;
        } else
        {
            //reach the end of the list and insert
            Node lastNode = head;
            //increment through nodes until reached end
            while(lastNode.next != null) {
                lastNode = lastNode.next;
            }

            // Insert the new node at the end
            lastNode.next = newNode;
        }

        size++;

        return true;
    }



    /**
     * Appends the specified element to the end of this list
     *
     * @param       data    int to add to the linked list
     *
     * @return              True if the element is added
     */
    public boolean add(Comparable data)
    {
        Node newNode = new Node(data); //create new node
        newNode.next = null;  //node has no next node

        if(head == null)
        {
            //there is no head node so set this node
            //to be the head node
            head = newNode;
        } else
        {
            //reach the end of the list and insert
            Node lastNode = head;
            //increment through nodes until reached end
            while(lastNode.next != null) {
                lastNode = lastNode.next;
            }

            // Insert the new node at the end
            lastNode.next = newNode;
        }

        size++;

        return true;
    }



    /**
     * Inserts the specified element at the specified position in this list
     *
     * @param       data    int to add to the linked list
     * @param		index	index to add the data to
     *
     * @return              True if the element is added
     */
    public void add(int index, Comparable element)
    {
        Node newNode = new Node(element);
        Node currNode = head;
        Node prevNode = null;

        //adding a new node as the head
        if(index == 0)
        {
            if(currNode != null)
            {
                newNode.next = currNode;
                head = newNode;
                size++;
                return;
            }
        }

        //check rest of nodes for index number to add
        int counter = 0;
        while(currNode != null)
        {
            if(counter == index)
            {
                //found the index to add, set the
                //new node's next to the current
                //node's next- to insert this node
                //newNode.next = currNode.next;
                //currNode.next = newNode;
                prevNode.next = newNode;
                newNode.next = currNode;
                size++;
                return;
            }
            else
            {
                //this isn't the index to add,
                //move on to the next index
                prevNode = currNode;
                currNode = currNode.next;
                counter = counter + 1;
            }
        }
    }



    /**
     * Removes all of the elements from this list
     *
     */
    public void clear()
    {
        //clear the list of all elements
        head = null;
        size = 0;
    }


    /**
     * Returns true if this list contains the specified element.
     *
     * @param       o	    int to check for within the list
     *
     * @return              True if the element is found
     */
    public boolean contains(Comparable o)
    {
        Node currNode = head;

        //loop through the nodes to find a match
        while(currNode != null)
        {
            if(currNode.data == o)
            {
                //this node matches the value given
                return true;
            }else {
                //the node doesn't match the value given
                currNode = currNode.next;
            }
        }
        return false;
    }

    /**
     * Returns true if this list contains the specified element.
     *
     * @param       o	    int to check for within the list
     *
     * @return              True if the element is found
     */
    public boolean containsCh(String o)
    {
        Node currNode = head;

        //loop through the nodes to find a match
        while(currNode != null)
        {
            if(currNode.ch.equals(o))
            {
                //this node matches the value given
                return true;
            }else {
                //the node doesn't match the value given
                currNode = currNode.next;
            }
        }
        return false;
    }


    /**
     * Returns the element at the specified position in this storage.
     *
     * @param       index   index of list to return value
     *
     * @return              int from the index given
     * 						if there is no index, return -1
     */
    @Override
    public Comparable get(int index)
    {
        int counter = 0;
        Node currNode = head;

        //go through each node
        while(currNode != null)
        {
            //check for match of target index and
            //current node index
            if (counter == index)
            {
                return currNode.data;
            }

            currNode = currNode.next;
            counter = counter + 1;
        }
        return -1;
    }

    /**
     * Returns the character element at the specified
     * position in this storage.
     *
     * @param       index   index of list to return value
     *
     * @return              int from the index given
     * 						if there is no index, return -1
     */
    @Override
    public Comparable getCh(int index)
    {
        int counter = 0;
        Node currNode = head;

        //go through each node
        while(currNode != null)
        {
            //check for match of target index and
            //current node index
            if (counter == index)
            {
                return currNode.ch;
            }

            currNode = currNode.next;
            counter = counter + 1;
        }
        return -1;
    }


    /**
     * Returns the character element at the specified
     * position in this storage.
     *
     * @param       index   index of list to return value
     *
     * @return              int from the index given
     * 						if there is no index, return -1
     */
    @Override
    public Comparable getCh(Comparable o)
    {
        int counter = 0;
        Node currNode = head;

        //go through each node
        while(currNode != null)
        {
            //check for match of target index and
            //current node index
            if (currNode.data.equals(o))
            {
                return currNode.ch;
            }

            currNode = currNode.next;
            counter = counter + 1;
        }
        return -1;
    }



    /**
     * Returns the Node at the specified position in this storage.
     *
     * @param       index   index of list to return value
     *
     * @return              node from the index given
     * 						if there is no node, return null
     */
    @Override
    public Node getLeft(int index)
    {
        int counter = 0;
        Node currNode = head;

        //go through each node
        while(currNode != null)
        {
            //check for match of target index and
            //current node index
            if (counter == index)
            {
                return currNode.left;
            }

            currNode = currNode.next;
            counter = counter + 1;
        }
        return null;
    }


    /**
     * Returns the Node at the specified position in this storage.
     *
     * @param       index   index of list to return value
     *
     * @return              node from the index given
     * 						if there is no node, return null
     */
    @Override
    public Node getRight(int index)
    {
        int counter = 0;
        Node currNode = head;

        //go through each node
        while(currNode != null)
        {
            //check for match of target index and
            //current node index
            if (counter == index)
            {
                return currNode.right;
            }

            currNode = currNode.next;
            counter = counter + 1;
        }
        return null;
    }

    /**
     * Returns the Node at the specified position in this storage.
     *
     * @param       index   index of list to return value
     *
     * @return              node from the index given
     * 						if there is no node, return null
     */
    @Override
    public Node getNode(int index)
    {
        int counter = 0;
        Node currNode = head;

        //go through each node
        while(currNode != null)
        {
            //check for match of target index and
            //current node index
            if (counter == index)
            {
                return currNode;
            }

            currNode = currNode.next;
            counter = counter + 1;
        }
        return null;
    }


    /**
     * Returns the index of the first occurrence of the specified
     * element in this list, or -1 if this list does not
     * contain the element.
     *
     * @param       o	    int to search for within the list
     *
     * @return              int index for the given value
     */
    public int indexOf(Comparable o) {
        int counter = 0;
        Node currNode = head;

        //go through each node
        while(currNode != null)
        {
            //return when the int is found
            if(currNode.data == o)
            {
                return counter;
            }
            counter = counter + 1;
            currNode = currNode.next;
        }
        return -1;
    }


    /**
     * Returns the index of the first occurrence of the specified
     * character in this list, or -1 if this list does not
     * contain the element.
     *
     * @param       o	    int to search for within the list
     *
     * @return              int index for the given value
     */
    public int indexOfCh(String o) {
        int counter = 0;
        Node currNode = head;

        //go through each node
        while(currNode != null)
        {
            //return when the int is found
            if(currNode.ch.equals(o))
            {
                return counter;
            }
            counter = counter + 1;
            currNode = currNode.next;
        }
        return -1;
    }

    /**
     * Returns the index of the last occurrence of the specified
     *  element in this list, or -1 if this list does not
     *  contain the element.
     *
     * @param       o	    int to search for within the list
     *
     * @return              int index for last time int seen
     */
    @Override
    public int lastIndexOf(Comparable o) {
        int counter = 0;
        Node currNode = head;
        int lastSeen = -1;

        //go through each node
        while(currNode != null)
        {
            //store the last index when this int
            //was found inside the list
            if(currNode.data == o)
            {
                lastSeen = counter;
            }
            counter = counter + 1;
            currNode = currNode.next;
        }
        return lastSeen;
    }

    /**
     *  Removes the first occurrence of the specified element
     *   from this list, if it is present.
     *
     * @param       o	    Comparable to remove from list
     *
     * @return              Comparable removed
     */
    @Override
    public boolean remove(Comparable o)
    {
        Node currNode = head;
        Node prevNode = null;

        //check head node to see if it has the data
        if(currNode != null && currNode.data.equals(o))
        {
            head = currNode.next;
            size--;
            return true;
        }

        //search other nodes for the int to delete
        while(currNode != null && !currNode.data.equals(o))
        {
            prevNode = currNode;
            currNode = currNode.next;
        }

        //the current node is the node to remove
        if(currNode != null)
        {
            prevNode.next = currNode.next;
            size--;
            return true;
        }

        //the value o hasn't been found among data
        if(currNode == null)
        {
            return false;
        }


        return false;
    }

    /**
     * Removes the element at the specified position in
     * this list (optional operation).
     *
     * @param       index	int remove from list
     *
     * @return              comparable object removed
     */
    @Override
    public Comparable remove(int index)
    {
        Node currNode = head;
        Node prevNode = null;

        //check head node, index 0, for deletion
        if(index == 0 && currNode !=null)
        {
            head = currNode.next;
            size--;
            return index;
        }

        //check rest of nodes for index number to delete
        int counter = 0;
        while(currNode != null)
        {
            if(counter == index)
            {
                //found the index to remove, set the
                //previous node's next to the current
                //node's next- to skip this node
                prevNode.next = currNode.next;
                size--;
                return index;
            }
            else
            {
                //this isn't the index to remove,
                //move on to the next index
                prevNode = currNode;
                currNode = currNode.next;
                counter = counter + 1;
            }
        }

        return index;

    }

    /**
     * Replaces the element at the specified position in
     * this list with the specified element
     *
     * @param       index	int for the location to set value
     * @param		data	data to set at the location
     *
     * @return              return Comparable set
     */
    @Override
    public Comparable set(int index, Comparable element)
    {
        Node newNode = new Node(element);
        Node currNode = head;
        Node prevNode = null;

        //adding a new node as the head
        if(index == 0)
        {
            if(currNode != null)
            {
                newNode.next = head.next;
                head = newNode;
                return index;
            }
        }

        //check rest of nodes for index number to add
        int counter = 0;
        while(currNode != null)
        {
            if(counter == index)
            {
                //found the index to add, set the
                //new node's next to the current
                //node's next- to insert this node
                //newNode.next = currNode.next;
                //currNode.next = newNode;
                prevNode.next = newNode;
                newNode.next = currNode.next;
                return index;
            }
            else
            {
                //this isn't the index to add,
                //move on to the next index
                prevNode = currNode;
                currNode = currNode.next;
                counter = counter + 1;
            }
        }


        //the position element wasn't found
        return -1;
    }


    /**
     * Replaces the element at the specified position in
     * this list with the specified element
     *
     * @param       index	int for the location to set value
     * @param		data	data to set at the location
     *
     * @return              return Comparable set
     */
    @Override
    public Comparable set(int index, Comparable element, String ch)
    {
        Node newNode = new Node(element, ch);
        Node currNode = head;
        Node prevNode = null;

        //adding a new node as the head
        if(index == 0)
        {
            if(currNode != null)
            {
                newNode.next = head.next;
                head = newNode;
                return index;
            }
        }

        //check rest of nodes for index number to add
        int counter = 0;
        while(currNode != null)
        {
            if(counter == index)
            {
                //found the index to add, set the
                //new node's next to the current
                //node's next- to insert this node
                //newNode.next = currNode.next;
                //currNode.next = newNode;
                prevNode.next = newNode;
                newNode.next = currNode.next;
                return index;
            }
            else
            {
                //this isn't the index to add,
                //move on to the next index
                prevNode = currNode;
                currNode = currNode.next;
                counter = counter + 1;
            }
        }


        //the position element wasn't found
        return -1;
    }

    /**
     * Replaces the element at the specified position in
     * this list with the specified element
     *
     * @param       index	int for the location to set value
     * @param		element	data to set at the location
     * @param 		ch		String value to set
     * @param		lNode	Left node to set
     * @param		rNode	Right node to set
     *
     * @return              return Comparable set
     */
    @Override
    public Comparable set(int index, Comparable element, String ch,
                          Object lNode, Object rNode)
    {
        Node newNode = new Node(element, ch, (Node)lNode, (Node)rNode);
        Node currNode = head;
        Node prevNode = null;

        //adding a new node as the head
        if(index == 0)
        {
            if(currNode != null)
            {
                newNode.next = head.next;
                head = newNode;
                return index;
            }
        }

        //check rest of nodes for index number to add
        int counter = 0;
        while(currNode != null)
        {
            if(counter == index)
            {
                //found the index to add, set the
                //new node's next to the current
                //node's next- to insert this node
                //newNode.next = currNode.next;
                //currNode.next = newNode;
                prevNode.next = newNode;
                newNode.next = currNode.next;
                return index;
            }
            else
            {
                //this isn't the index to add,
                //move on to the next index
                prevNode = currNode;
                currNode = currNode.next;
                counter = counter + 1;
            }
        }


        //the position element wasn't found
        return -1;
    }



}
