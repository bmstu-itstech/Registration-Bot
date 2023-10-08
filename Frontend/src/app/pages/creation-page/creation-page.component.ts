import {Component, ElementRef, HostListener, Input, OnInit, ViewChild} from '@angular/core';
import {JsonHandlerService} from "../../service/json-handler.service";
import {Edge, Layout, Node} from "@swimlane/ngx-graph";
import {DagreNodesOnlyLayout} from "@swimlane/ngx-graph"
import * as shape from 'd3-shape';
import {Subject} from "rxjs";

export class QuestionBlock {
  id!: string;
  name!: string;
  upperManagerId?: string;
}
interface CustomNode extends Node {
  isSelected?: boolean;
}

@Component({
  selector: 'app-creation-page',
  templateUrl: './creation-page.component.html',
  styleUrls: ['./creation-page.component.scss']
})
export class CreationPageComponent implements OnInit {
  @ViewChild('graph', { static: true }) graph!: ElementRef;
  scrollHeightPercentage = 100;
  isDragging = false;
  startY = 0;
  startScrollTop = 0;
  update$: Subject<boolean> = new Subject();
  center$: Subject<boolean> = new Subject();
  zoomToFit$: Subject<boolean> = new Subject();
  @Input() questionBlocks: QuestionBlock[] = [];
  public nodes: Node[] = [];
  public links: Edge[] = [];
  public selectedNodes: CustomNode[] = [];
  public layoutSettings = {
    orientation: 'TB'
  };
  public layout: Layout = new DagreNodesOnlyLayout();
  public curve: any = shape.curveLinear;
  constructor(private jsonHandlerService: JsonHandlerService) {
    const jsonData = this.jsonHandlerService.getJsonData();
    this.questionBlocks = [
      {
        id: '1',
        name: 'Начало',
      },
      {
        id: '2',
        name: 'Employee 2',
        upperManagerId: '1'
      },
      {
        id: '3',
        name: 'Employee 3',
        upperManagerId: '1'
      },
      {
        id: '4',
        name: 'Employee 4',
        upperManagerId: '2'
      },
      {
        id: '5',
        name: 'Employee 5'
      }
    ];
  }
  public ngOnInit() {
    const savedLinks = localStorage.getItem('graphLinks');
    if (savedLinks) {
      this.links = JSON.parse(savedLinks);
    } else {
      for (const questionBlock of this.questionBlocks) {
        if (!questionBlock.upperManagerId) {
          continue;
        }
        const edge: Edge = {
          source: questionBlock.upperManagerId,
          target: questionBlock.id,
          label: ''
        };
        this.links.push(edge);
      }
    }
    for (const questionBlock of this.questionBlocks) {
      const node: Node = {
        id: questionBlock.id,
        label: questionBlock.name
      };
      this.nodes.push(node);
    }
  }
  deleteEdge(sourceNodeId: string, targetNodeId: string) {
    const edgeIndex = this.links.findIndex(edge => edge.source === sourceNodeId && edge.target === targetNodeId);
    if (edgeIndex !== -1) {
      this.links.splice(edgeIndex, 1);
      this.updateGraph();
      localStorage.setItem('graphLinks', JSON.stringify(this.links));
    }
  }
  updateGraph() {
    this.update$.next(true)
  }
  centerGraph() {
    this.center$.next(true);
  }
  fitGraph() {
    this.zoomToFit$.next(true)
  }
  onNodeClick(selectedNode: CustomNode) {
    const index = this.selectedNodes.findIndex(node => node.id === selectedNode.id);
    if (index != -1) {
      this.selectedNodes.splice(index, 1);
    } else {
      this.selectedNodes.push(selectedNode);
      selectedNode['isSelected'] = true;
    }
    this.createEdgeIfNeeded();
  }
  createEdgeIfNeeded() {
    if (this.selectedNodes.length === 2) {
      const sourceNode = this.selectedNodes[0];
      const targetNode = this.selectedNodes[1];
      const existingEdge = this.links.find(edge => edge.source === sourceNode.id && edge.target === targetNode.id
        || edge.source === targetNode.id && edge.target === sourceNode.id);
      if (!existingEdge) {
        const newEdge: Edge = {
          source: sourceNode.id,
          target: targetNode.id,
          label: ''
        }
        this.links.push(newEdge);
        localStorage.setItem('graphLinks', JSON.stringify(this.links));
        this.updateGraph();
      }
      this.selectedNodes.forEach(node => delete node['isSelected']);
      this.selectedNodes = [];
    }
  }
  onScrollLineMouseDown(event: MouseEvent) {
    this.isDragging = true;
    this.startY = event.clientY;
    this.startScrollTop = this.graph.nativeElement.scrollTop;
  }

  @HostListener('document:mousemove', ['$event'])
  onMouseMove(event: MouseEvent) {
    if (this.isDragging) {
      const deltaY = event.clientY - this.startY;
      const newScrollTop = this.startScrollTop + deltaY;

      // Ограничиваем новую позицию скролла
      if (newScrollTop >= 0 && newScrollTop <= this.graph.nativeElement.scrollHeight - this.graph.nativeElement.clientHeight) {
        this.graph.nativeElement.scrollTop = newScrollTop;
        this.calculateScrollHeightPercentage();
      }
    }
  }

  @HostListener('document:mouseup')
  onMouseUp() {
    this.isDragging = false;
  }

  private calculateScrollHeightPercentage() {
    const maxScrollTop = this.graph.nativeElement.scrollHeight - this.graph.nativeElement.clientHeight;
    this.scrollHeightPercentage = (this.graph.nativeElement.scrollTop / maxScrollTop) * 100;
  }
  isSectionVisible = true;
  addJsonQuestion() {
    const currentQuestionNumber = this.jsonHandlerService.getCurrentQuestionNumber()
    const newQuestionKey = (currentQuestionNumber).toString();
    const newData = {
      [newQuestionKey]: {
        "question": "",
        "answer_type": "",
        "title": "",
        "buttons": [],
        "next_id": null
      }
    }
    this.jsonHandlerService.updateJsonDataModules(newData);
    const updatedQuestionNumber = currentQuestionNumber + 1;
    this.jsonHandlerService.saveCurrentQuestionNumber(updatedQuestionNumber);
    this.isSectionVisible = !this.isSectionVisible;
  }
}
