<div align="center">
  <h1>CASCADE</h1>
</div>

<br>

<div>
  <h1>About Cascade</h1>
  <p>
    CascadeV4 is a high-level dynamic programming language, revamped for the 4th time to make more extensive use of OOP. To run any file, just write any file ending in .csc in Cascade syntax and then run the main.py file.
    <ul>
      <li>Lexer: Program File -> Token Stream</li>
      <li>Parser: Token Stream -> AST</li>
      <li>Interpreter: AST > Execution</li>
    </ul>
  </p>
</div>

<br>
<br>

<h1>Syntax</h1>
  <p>
    Declaring/Modifying Variables
    <ul>
      <li>var x = 1</li>
      <li>x = 1</li>
    </ul>
  </p>

  <p>
    Declaring/Modifying Hypervariables
    <ul>
      <li>hvar x (y z) = y + z</li>
      <li>x (y z) := y + z</li>
      <li>x := y + z // arguments are autocompleted</li>
    </ul>
  </p>

  <p>
    For Statements
    <ul>
      <li>for x in 1..10 { ... }</li>
      <li>for x in 1..y { ... }</li>
    </ul>
  </p>

  <p>
    While Statements
    <ul>
      <li>while x > y { ... }</li>
    </ul>
  </p>

  <p>
    If Statements
    <ul>
      <li>if x > y { ... }</li>
    </ul>
  </p>
  
  <p>
    Comments
    <ul>
      <li>// This is a comment</li>
    </ul>
  </p>

  <p>
    Multi-line Comments
    <ul>
      <li> Example in code, HTML formatting messing it up </li>
    </ul>
  </p>

  <p>
    Expressions
    <ul>
      <li> (2*x) + (3*y) </li>
      <li> 2*x + 3*y //autobidmas </li>
      <li> 2x + 3y //mathematics notation, however cannot do ab, since it is interpreted as a new variable, ab</li>
    </ul>
  </p>

  <p>
    Expressions
    <ul>
      <li> IMPROVED ERROR MESSAGES: COMING EXTREMELY SHORTLY!!!!!!!!!! </li>
      <li> LIBRARIES: COMING VERY SOON!!!!! </li>
      <li> WHEN STATEMENTS: COMING SOON! </li>
      <li> ONCE STATEMENTS: COMING LESS SOON... </li>
      <li> FUNCTIONS: COMING EVENTUALLY... PROBABLY. </li>
      <li> OOP: COMING... PROBABLY NEVER. </li>
    </ul>
  </p>
  

  


<div>
  <h2>maincode</h2>
  <p>
    Contains all key folders 
  </p>
</div>

<div>
  <h2>core</h2>
  <p>
    contains the main files for tokenising, parsing, and interpreting
  </p>
</div>

<div>
  <h2>dataReference</h2>
  <p>
    Contains the files for bulk data lookup
  </p>
</div>

<div>
  <h2>validation</h2>
  <p>
   Contains any files for validating data present
  </p>
</div>










