/**
 * version
 * 2
 * implmented all functions from IntegerStorage
 * prefomed bug fixes
 */


/**
 * Generics notes week 6
 * these are templates exept you can't use them with primative types,
 * they let you pass along specfic values
 * E-elements
 * K-key
 * N-numer
 * t-type
 * V-Value
 * we can specify what valable we want the generic to have when we in statate the
 * object via<varable> all have to be instanated as the
 * all generics have to be specified on constuction
 *raw types, a valueless type that just placeholds somthing in memory
 * (don't use these)
 *type easire?
 * box<int> boxint= new box<> does work
 *vector?
 * can have muiltiple types of generics aka <E, V>  and that is how they are declared *
 *= bettween diffrent generics doesn't work becuase the object with a diffrent generic could
 * instante objects that don't work under the generic it has been set equal to
 * can have a generic extend other classes which will give your type T access to all tools that the class
 * did
 * can extend multiple classes via a{class/interface} & b(interface) & c(interface) overwideing memthodes from left to right (left is instantated frist)
 * generices can't create static feilds they cant have instances of type paramiaters (not by themselves)
 * can't chatch or throw objects of param type
 * for gennertics Wildcards are ?'s gives you access to all subclasses you bound into it
 * how does this effect passed types
 *extends does everything nesxt to what you call and up
 * super does the opiste
 *
 *
 *
 *
 *
 * author Luke Batchelder Jessica
 */
public class AugmentedVector<T> implements IntegerStorage {
    T[] container;

    /**creates our container and it's ints
     *
     * @param size: how large we want the starting vector to be
     */
    AugmentedVector(int size) {
        container = new T[size];
    }

    /**
     * default constuctor, inlizized at 0
     */
    AugmentedVector() {
        container = new int[0];
    }

    /**
     * helper function for the add functions in this program, adds a number of
     * elements to a given point in the array by recreateding a newly sized array
     * @param location: where we will place them
     * @param spaces: how many elements will there be
     * @param newValues: the new values we will be adding
     */
    void insert(int location, int spaces, int[] newValues) {
        int oldLength = container.length;
        int ajustedSize = 0;
        int[] containerCopy = new int[(oldLength + newValues.length)];
        boolean inemptySpace = false;
        //creates the values within the copyed container staring with those before the insert
        for (int i = 0; i < containerCopy.length; i++) {
            if (i == location) {
                inemptySpace = true;
            }
            if (inemptySpace == false) {
                containerCopy[i] = container[i - ajustedSize];
            }
            //if we are in the space we should insert in we will then insert all new values
            else {
                for (int m = 0; m < spaces; m++, i++) {
                    containerCopy[i] = newValues[m];
                }
                //passes back the varables to the rest of the loop to ensure remaining values are copyed correctly
                ajustedSize=spaces;
                i--;
                inemptySpace = false;
            }
        }
        //sets our container to the newly made one
        container = containerCopy;

    }

    /** Appends the specified element to the end of this list
     *
     * @param o: int we are adding to the end of the list
     * @return weather or not we successfully added the element
     */
    public boolean add(int o) {
        int[] addednumber = {o};
        insert(container.length, 1, addednumber);
        return true;
    }

    /** Inserts the specified element at the specified position in this list
     *
     * @param index: point we are adding the element
     * @param element: element we are adding
     */
    public void add(int index, int element) {
        int[] addednumber = {element};
        insert(index, 1, addednumber);
    }

    // Appends all of the elements in the specified array to the end of this list, in the same order that
    // they appear in the array
    public boolean addAll(int[] os) {
        insert(container.length, os.length, os);
        return true;
    }

    // Inserts all of the elements in the specified collection into this list at the specified position
    public boolean addAll(int index, int[] os) {
        insert(index, os.length, os);
        return true;
    }

    // Removes all of the elements from this list
    public void clear() {
        container=new int[0];

    }

    /**
     *
     * @param o= int passed by program
     * @return Returns true if this list contains the specified element.
     */
    public boolean contains(int o) {
        for (int i = 0; i < container.length; i++) {
            if (container[i] == o)
                return true;
        }
        return false;
    }

    /**
     *
     * @param os= array of ints
     * @return true if this list contains all of the elements of the specified collection.
     */
    public boolean containsAll(int[] os) {
        int osCount = 0;
        for (int i = 0; i < container.length; i++) {
            if (container[i] == os[osCount]) {
                osCount++;
            } else {
                osCount = 0;
            }
            if (osCount == os.length)
                return true;
        }
        return false;
    }

    /** Compares the specified object with this storage for equality.
     *
     * @param o=object passed by program
     * @return weather or not the memory location is identical
     */
    public boolean equals(Object o) {
        if (o == this)
            return true;
        else
            return false;
    }

    /** Compares the specified IntegerStorage for content equality
     * both in terms of values and order.
     *
     * @param o=integerStorage we are compairing
     * @return: weather or not they are equal in terms of both in terms of values and order.
     */
    public boolean contentEquals(IntegerStorage o) {
        if (o.size() != container.length) {
            return false;
        }
        for (int i = 0; i < container.length; i++) {
            if (o.indexOf(i) != container[i])
                return false;
        }
        return true;
    }

    /** Returns the element at the specified position in this storage.
     *
     * @param index: location we want the element from as given by the user
     * @return the element at the given location
     */
    public int get(int index) {
        return container[index];
    }

    /** Returns the hash code value for this storage.
     *  Defined as the sum of the elements in the storage
     */
    public int hashCode() {
        int sum = 0;
        for (int i = 0; i < container.length; i++)
            sum += container[i];
        return sum;
    }

    /** Returns the index of the first occurrence of the specified element
     * in this list, or -1 if this list does not contain the element.
     *
     * @param o: number we are trying to find the index of
     * @return location of the int if it is in the array, -1 otherwise
     */
    public int indexOf(int o) {
        int i = 0;
        while (i < container.length) {
            if (container[i] == o) {
               return i;
            }
            i++;
        }
            return -1;
    }

    /**Returns true if this storage contains no elements.
     *
     * @return true if the function has no elements, false otherwise
     */
    public boolean isEmpty() {
        if (container == null || container.length==0)
            return true;
        else
            return false;
    }


    /**
     * Returns the index of the last occurrence of the specified element in this list,
     * or -1 if this list does not contain the element.
     * @param o: number we are trying to find the index of
     * @return: -1 if int is not in our array or the postion of o if it is
     */
    public int lastIndexOf(int o) {
        int finalIndex = -1;
        for (int i = 0; i < container.length; i++) {
            if (container[i] == o)
                finalIndex = i;
        }
        return finalIndex;
    }

    /**
     * helper function for the remove functions reused some elements of insert here
     * @param location: location elements are to be deleted from
     * @param elementsRemoved: the number of elements that will be removed
     */
    public void deleteListElement(int location, int elementsRemoved) {
        int oldLength = container.length;
        int ajustedSize = 0;
        //simliar to the insert function we needed to create a copy of the list
        int[] containerCopy = new int[(oldLength - elementsRemoved)];
        boolean inemptySpace = false;
        //simliar to insert we needed to increment thought it and copy values
        for (int i = 0; i < containerCopy.length; i++) {
            if (i == location && ajustedSize==0) {
                inemptySpace = true;
            }
            if (inemptySpace == false)
                containerCopy[i] = container[i + ajustedSize];
            //the diffrence being that this time we just need to advance though our
                // orignal array and exclude certain elements from being in the new one
            else {
                inemptySpace = false;
                ajustedSize = 1;
                i--;
            }
        }
        container = containerCopy;

    }

    /**
     * removes the object in the array at o location
     * @param o: int provided by the user
     * @return 0 if all objects in os were in the array -1 if any were not
     */
    public int remove(int o) {
        if(o>=container.length)
            return -1;
        deleteListElement(o,1);
        return 0;
    }

    /**
     * removes the integer o from the array
     * @param o: integer given by the user
     * @return true if all objects were in the array false if they were not
     */
    public boolean	remove(Integer o){
        int location = -1;
        int i = 0;
        while (location == -1 && i < container.length) {
            if (o == container[i])
                location = i;
            i++;
        }
        if (location > -1) {
            deleteListElement(location, 1);
            return true;
        } else {
            return false;
        }
    }

    /**
     *
     * @param os: an array of integer objects passed to us by the program
     * @return true if all objects in os were in the array false if any where not
     */
    public boolean removeAll(int[] os) {
        int location = -1;
        int i = 0;
        boolean anyremoved=false;
        //runs for each element in os
        for (int m = 0; m < os.length; m++) {
            //runs though container and deletes the frist occurance it finds of os[m]
            while (location == -1 && i < container.length) {
                if (os[m] == container[i])
                    location = i;
                i++;
            }
            //if element was not in the array it stops the function and returns false
            if (location > -1) {
                deleteListElement(location, 1);
                i = 0;
                location = -1;
                anyremoved=true;
            }
        }
        //returns true if all elements were deleted
        return anyremoved;
    }

    /**
     * @param index:   element of the contatiner we wish to change
     * @param element: element we wish to change it to
     * @return: a 0 if the proccess was successful and a -1 if it was not aka was in range of function
     */
    public int set(int index, int element) {
        if (index < container.length) {
            container[index] = element;
            return 0;
        } else {
            return -1;
        }
    }

    /**
     * Returns the number of elements in this storage.
     *
     * @return: size of the array in use
     */
    public int size() {
        return container.length;
    }

    /**
     * prints out all values of the array in a visually appealing fasion
     * @return string containing all objects spearated by a space
     */

    public String toString() {
        String displayString = "{";
        if(container.length>0){
            //sorts though the array and deplays each member
            for (int i = 0; i < container.length-1; i++) {
                displayString = displayString + container[i] + ", ";
            }
            displayString=displayString+container[container.length-1];
        }
        return displayString+"} ";
    }


    /** Sorts this storage into ascending order.
     * aim to use mergsort/quicksort in industral grade implemenation
     *
     */
    public void sort() {
        //runs a basic sort algorithm, not time efficient but functional for this project
        for (int i = 0; i < container.length; i++) {
            for (int m = i; m < container.length; m++) {
                if (container[i] > container[m]) {
                    int containerCopy = container[i];
                    set(i, container[m]);
                    set(m, containerCopy);
                }
            }

        }


    }


}


