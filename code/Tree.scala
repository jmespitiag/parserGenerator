package Tree
import scala.math._
sealed trait Tree[+A]
case class Leaf[A](value:A) extends Tree[A]
case class Branch[A](value:A, left:Tree[A],right:Tree[A]) extends Tree[A]


object Tree
{
  def inorder_recursive(t : Tree[String]): Int = {
    t match {
      case Branch(v, left, right) if (v=="+") =>
        return inorder_recursive(left) + inorder_recursive(right)
      case Branch(v, left, right) if (v=="-") =>
        return inorder_recursive(left) - inorder_recursive(right)
      case Branch(v, left, right) if (v=="*") =>
        return inorder_recursive(left) * inorder_recursive(right)
      case Branch(v, left, right) if (v=="/") =>
        return inorder_recursive(left) / inorder_recursive(right)
      case Branch(v, left, right) if (v=="#") => var leftVal = inorder_recursive(left)
      var rightVal = inorder_recursive(right)
      if (leftVal>=rightVal){return scala.math.pow(leftVal,rightVal).toInt}
      else{return leftVal / rightVal}
  
      case Leaf(v) =>
        return v.toInt
    }
  }
  

  def check_op[A](x:A): Boolean =
  {
    if (x=="*" || x=="+" || x=="-" || x=="/" || x=="#")
    {
      return true
    }
    else{return false}
  }

  def convertTree(lst:Array[String]): (Tree[String],Array[String]) =
  {
    if (lst.isEmpty){return (Leaf(""),lst)}
    val i = lst(0)
    if (check_op(i))
    {
      val tree1 = convertTree(lst.slice(1,lst.length))
      val t = tree1._1
      val ls = tree1._2
      val tree2 = convertTree(ls)
      val t1 = tree2._1
      val ls1 = tree2._2
      return (Branch(i,t,t1),ls1)
    }
    else
    {
      return (Leaf(i),(lst.slice(1,lst.length)))
    }
  }
}

