package Tree
import scala.io.StdIn.readLine
object mainaux{
  def calculatePrefix():Int={
    val line = readLine("Enter an operation on prefix notation: ")
    val notation = line.split("")
    val values = Tree.convertTree(notation)
    val tree = values._1
    val result = Tree.inorder_recursive(tree)
    return result
  }
}